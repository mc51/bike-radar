"""Booking stuff"""
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import geopy.distance  # type: ignore

from pages.src import config
from pages.src.api import Api

log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)

MAX_BIKES = config.MAX_BIKES


class Booking:  # pylint: disable=too-many-instance-attributes
    """Booking"""

    id: int
    place_id: int
    place_name: str
    lat: float
    lng: float
    bike_blocking_time_seconds: int
    start_time: int
    booking_code: int
    state_id: int
    distance: int | None = None
    booked: bool = False
    timezone: str = "UTC"

    def __init__(self, api: Api | None = None, store_data: dict | None = None):
        """
        Initialize class using api object and store data if available.

        Args:
            api (Api | None, optional): Api. Defaults to None.
            store_data (dict | None, optional): Store data. Defaults to None.
        """
        self.api = Api()
        if api:
            self.api = api

        self.current_booking = self.get_last_booking()
        if self.current_booking:
            for key, value in self.current_booking.items():
                setattr(self, key, value)

        if store_data and self.is_active:
            self.timezone = store_data["timezone"]
            self.distance = self.get_distance_from_coords(
                lat=store_data["lat"], lng=store_data["lon"]
            )
            log.debug(
                "Distance and timezone for current booking: %s, %s",
                self.distance,
                self.timezone,
            )

    def get_distance_from_coords(self, lat: float, lng: float) -> int:
        """Get distance in m from specified coordinates to current booking.

        Args:
            lat (float): lat
            lng (float): lng

        Returns:
            int: distance
        """
        return int(geopy.distance.distance((self.lat, self.lng), (lat, lng)).meters)

    def get_bookings(self) -> dict:
        """Get all bookings.

        Returns:
            dict: bookings
        """
        log.info("Getting all bookings.")
        bookings = self.api.request_bookings()
        return bookings

    def get_last_booking(self) -> dict | None:
        """Get last booking.

        Returns:
            dict | None: booking
        """
        log.debug("Getting last booking.")
        bookings = self.get_bookings()
        if bookings.get("items"):
            return bookings["items"][-1]
        return None

    @property
    def is_active(self) -> bool:
        """Is booking active.

        Returns:
            bool: is active
        """
        if self.state_id == 5:
            return True
        return False

    def to_status(self) -> str:
        """Convert booking to status string.

        Returns:
            str: status
        """
        msg = "You have no active bookings. "
        if self.is_active:
            until = datetime.fromtimestamp(
                self.start_time + self.bike_blocking_time_seconds,
                tz=ZoneInfo(self.timezone),
            )
            until = until.strftime(config.BOOKING_TIME_FORMAT)
            msg = f"Booked {self.place_name} in {self.distance} m distance until {until}. "
        return f"Status: {msg}"
