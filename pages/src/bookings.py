"""Booking stuff"""
import logging
from datetime import datetime, timezone

import geopy.distance  # type: ignore

from pages.bike_radar import config
from pages.bike_radar.api import api

log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)

MAX_BIKES = config.MAX_BIKES


class Bookings:  # pylint: disable=too-many-instance-attributes
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

    def __init__(self, radar_status: dict | None = None):
        """bike booking

        Args:
            radar_status (dict | None, optional): Radar status. Defaults to None.
        """
        self.api = api
        self.current_booking = self.get_last_booking()
        if self.current_booking:
            for key, value in self.current_booking.items():
                setattr(self, key, value)
        if radar_status and self.is_active:
            log.info("Getting distance for current booking.")
            self.distance = self.get_distance_from_coords(
                lat=radar_status["lat"], lng=radar_status["lon"]
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
        log.info("Getting last booking.")
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
        msg = "You have no active bookings"
        if self.is_active:
            # todo: get timezone from user account and display in local time
            until = datetime.fromtimestamp(
                self.start_time + self.bike_blocking_time_seconds, tz=timezone.utc
            )
            msg = (
                f"Booked {self.place_name} in {self.distance} m distance until {until}."
            )
        return f"Status: {msg}"
