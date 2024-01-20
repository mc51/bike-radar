"""Locations stuff"""
import json
import logging
import sqlite3

import geopy.distance  # type: ignore

from pages.src import config
from pages.src.api import Api
from pages.src.bookings import Booking

log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)

MAX_BIKES = config.MAX_BIKES


class Locations:  # pylint: disable=too-many-instance-attributes
    """Locations class."""

    def __init__(self, store_data: dict | None = None):
        log.debug("Locations")

        self.store_data = store_data
        login_key = store_data["login_key"] if store_data else None
        self.api = Api(login_key)
        self.db_con = sqlite3.connect(config.DB_NAME)

        self.locations: dict[str, list]
        self.countries: list
        self.cities: list
        self.places: list
        self.cities_with_bikes: list
        self.bikes: list

        self.update_locations()

    def get_all_locations(self) -> dict[str, list]:
        """Get all locations data.

        Returns:
            dict[str, list]: locations
        """
        log.debug("Getting all locations data.")
        con = self.db_con
        try:
            with con:
                results = con.execute(f"select data from {config.DB_TABLE}")
                data = results.fetchone()
        except sqlite3.Error:
            log.exception("ERROR: reading data from db.")
            raise
        log.debug("OK: read data from db.")
        return json.loads(data[0])

    def get_bikes_in_city(self, city_id: int) -> list:
        """Get bikes in city.

        Args:
            city_id (int): city id

        Returns:
            list: places
        """
        log.debug("Getting bikes in city: %s.", city_id)
        return [bike for bike in self.bikes if bike["city_id"] == city_id]

    def update_locations(self):
        """Update all locations data."""
        log.debug("Updating all locations data.")
        self.locations = self.get_all_locations()
        self.countries = self.locations["countries"]
        self.cities = self.locations["cities"]
        self.places = self.locations["places"]
        self.cities_with_bikes = self.filter_for_cities_with_bikes(self.cities)
        self.bikes = self.filter_for_places_with_bikes(self.places)

    def get_timezone_for_city(self, city_id: int) -> str:
        """Get timezone for city from countries information.

        Args:
            city_id (int): city id

        Returns:
            str: timezone
        """
        log.debug("Getting timezone for city id: %s.", city_id)
        domain = [x["domain"] for x in self.cities if x["uid"] == city_id][0]
        timezone = [x["timezone"] for x in self.countries if x["domain"] == domain][0]
        log.debug("Domain: %s, Timezone: %s.", domain, timezone)
        return timezone

    def get_city_from_name(self, city: str) -> dict:
        """Get city by name.

        Args:
            city (str): city name

        Returns:
            dict: city
        """
        log.debug("Getting city by name.")
        for c in self.cities:
            if c["name"] == city:
                return c
        return {}

    def get_city_names(self) -> list[str]:
        """Get city names.

        Returns:
            list[str]: names
        """
        log.debug("Getting city names.")
        cities = self.cities_with_bikes
        return sorted([city["name"] for city in cities])

    def filter_for_cities_with_bikes(self, cities: list) -> list[dict]:
        """Filter for cities with bikes.

        Args:
            cities (list): cities

        Returns:
            list[dict]: cities with bikes
        """

        log.debug("Filtering for cities with bikes.")
        return [city for city in cities if city["available_bikes"] > 0]

    def filter_for_places_with_bikes(self, places: list) -> list[dict]:
        """Filter for places with available bikes.

        Args:
            places (list): places

        Returns:
            list[dict]: places with bikes
        """
        log.debug("Filtering places for bikes only.")
        return [p for p in places if p["bikes_available_to_rent"] > 0]

    def has_active_bookings(self, bookings) -> bool:
        """Check for active bookings.

        Returns:
            bool: True if active bookings, False if not
        """
        log.debug("Checking for active bookings.")
        if not bookings.get("items"):
            log.debug("No bookings found.")
            return False
        if bookings["items"][-1]["state_id"] == 5:
            log.debug("Active bookings found.")
            return True
        log.debug("No active bookings found.")
        return False

    def get_near_bikes(self, radius: int, lat: float, lon: float, city_id: int) -> list:
        """Get nearest bikes that are within distance.

        Args:
            radius (int): set radius
            lat (float): set lat
            lon (float): set lon
            city_id (int): city id

        Returns:
            list: nearest bikes
        """
        log.debug(
            "Getting nearest bikes for lat %s lon %s within radius %s in city id %s.",
            lat,
            lon,
            radius,
            city_id,
        )
        bikes = self.get_bikes_in_city(city_id)
        near_bikes = []
        for bike in bikes:
            if bike["bikes_available_to_rent"] > 0:
                distance = geopy.distance.distance(
                    (bike["lat"], bike["lng"]), (lat, lon)
                ).meters
                if distance <= radius:
                    bike["distance"] = round(distance)
                    near_bikes.append(bike)
        near_bikes = sorted(near_bikes, key=lambda d: d["distance"])[0:MAX_BIKES]
        log.debug(near_bikes)
        return near_bikes

    def get_booking_info(self, place_id: int) -> dict:
        """Get booking info.

        Args:
            place_id (int): place id

        Returns:
            dict: booking info
        """
        log.debug("Getting booking info for place %s.", place_id)
        info = self.api.request_booking_info(place_id=place_id)
        return info

    def cancel_booking(self, booking_id: int) -> bool:
        """Cancel booking.

        Args:
            booking_id (int): booking id

        Returns:
            bool: is canceled
        """
        log.debug("Cancelling booking with id %s.", booking_id)
        response = self.api.request_booking_cancellation(booking_id=booking_id)
        if response.get("booking", {}).get("canceled"):
            return True
        return False

    def book_bike(self, place_id: int) -> dict | None:
        """Book a bike. If another booking is already active, cancel first.

        Args:
            place_id (int): place id

        Returns:
            dict | None: booking status
        """
        log.info("Booking bike %s.", place_id)
        current_booking = Booking(self.api, self.store_data)
        if current_booking.is_active:
            log.debug("There already is an active booking. Canceling it first.")
            if not self.cancel_booking(booking_id=current_booking.id):
                log.error("Could not cancel current booking.")
                return None
            log.debug("Current booking cancelled.")

        booking = self.api.request_bike_booking(place_id=place_id)
        if booking.get("booking"):
            log.debug("Booking successful.")
            return booking["booking"]
        log.warning("Booking could not be finished.")
        return None

    def should_be_booked(self, bike: dict) -> bool:
        """Determine if bike should be booked.

        Args:
            bike (dict): bike

        Returns:
            bool: is booked
        """
        booking = Booking(self.api, self.store_data)
        if booking.distance and bike["distance"] >= booking.distance:
            log.debug(
                "Bike distance %s not closer than current booking %s.",
                bike["distance"],
                booking.distance,
            )
            return False
        log.debug(
            "Bike should be booked. Booking distance %s bike distance %s",
            booking.distance,
            bike["distance"],
        )

        booking_info = self.get_booking_info(bike["uid"])
        try:
            if booking_info["place"]["bike_types"][0]["available"] == 1:
                return True
        except IndexError:
            log.warning("Bike can only be rented but not booked.")
        return False

    def start_booking_process(self) -> Booking:
        """Start booking process. Use store data to recreate client state.

        Returns:
            BikeBooking: bike booking
        """
        log.info("Starting booking process.")

        assert self.store_data, "No store data."

        near_bikes = self.get_near_bikes(
            radius=self.store_data["radius"],
            lat=self.store_data["lat"],
            lon=self.store_data["lon"],
            city_id=self.store_data["city_id"],
        )
        if not near_bikes:
            log.info("No near bikes found.")
        else:
            log.info("Found near bikes.")

        for bike in near_bikes:
            if self.should_be_booked(bike):
                self.book_bike(bike["uid"])
                break
            log.info("Bike should not be booked.")
        else:
            log.info("No (new) bikes booked.")
        return Booking(self.api, self.store_data)
