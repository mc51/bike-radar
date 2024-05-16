"""Utilities"""

import re
from logging import Formatter
from pathlib import Path

from dash_leaflet import GeoJSON, Marker
from dash_leaflet.express import dicts_to_geojson

from pages.src.bookings import Booking


def get_version() -> str:
    """Get version of from pyproject.toml file.

    Returns:
        str: version
    """
    version = "0.1.0"
    lines = Path("pyproject.toml").read_text(encoding="utf8").splitlines()
    for line in lines:
        if "version" in line:
            version = re.findall(r'"([^"]*)"', line)[0]
            break
    return version


def create_bike_markers(
    bikes: list[dict], city_id: int, current_booking: Booking | None = None
) -> list[GeoJSON | Marker | None]:
    """Create clustered geo json markers for bike locations in city.

    Args:
        bikes (list[dict]): bikes
        city_id (int): city id
        current_booking (Booking | None): current booking. Defaults to None.

    Returns:
        list[GeoJSON | Marker | None]: markers
    """
    booked_bike = None
    if current_booking and current_booking.is_active:
        booked_bike = Marker(
            position=[current_booking.lat, current_booking.lng],
            icon={
                "iconUrl": "/assets/red_pin.webp",
                "iconSize": [56, 79],
                "iconAnchor": [28, 79],
                "zIndexOffset": 100,
            },
            title=f"Booked bike: {current_booking.place_name}",
        )

    bikes = [
        {"lat": b["lat"], "lon": b["lng"]} for b in bikes if b["city_id"] == city_id
    ]

    available_bikes = GeoJSON(
        data=dicts_to_geojson(bikes),
        interactive=False,
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
