"""Utilities"""
import re
from logging import Formatter

from dash_leaflet import GeoJSON, CircleMarker
from dash_leaflet.express import dicts_to_geojson

from pages.src.bookings import Booking


def create_bike_markers(
    bikes: list[dict], city_id: int, current_booking: Booking | None = None
) -> list[GeoJSON | CircleMarker | None]:
    """Create clustered geo json markers for bike locations in city.

    Args:
        bikes (list[dict]): bikes
        city_id (int): city id
        current_booking (Booking | None): current booking. Defaults to None.

    Returns:
        list[GeoJSON | CircleMarker | None]: markers
    """
    booked_bike = None
    if current_booking:
        lat = current_booking.lat
        lon = current_booking.lng
        booked_bike = CircleMarker(center=[lat, lon], radius=50)

    bikes = [
        {"lat": b["lat"], "lon": b["lng"]} for b in bikes if b["city_id"] == city_id
    ]
    available_bikes = GeoJSON(
        data=dicts_to_geojson(bikes),
        cluster=True,
        superClusterOptions={"radius": 100},
    )
    return [available_bikes, booked_bike]


class RedactingFormatter(Formatter):  # pylint: disable=too-few-public-methods
    """Redact sensitive strings from logs."""

    def __init__(self, orig_formatter):  # pylint: disable=super-init-not-called
        self.orig_formatter = orig_formatter
        self.patterns = ["email", "mobile", "loginkey", "login_key", "pin"]

    def format(self, record) -> str:
        """Format record by replacing all values of keys corresponding to pattern.

        Args:
            record (_type_): record

        Returns:
            str: redacted message
        """
        msg: str = self.orig_formatter.format(record)
        msg = msg.replace("'", '"')

        for pattern in self.patterns:
            p = rf'"{pattern}":\s*"([^"]+)"'
            match = re.search(p, msg)
            if match:
                secret = match.group(1)
                msg = msg.replace(str(secret), "***redacted***")
        return msg

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)
