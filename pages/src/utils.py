"""Utilities"""
from logging import Formatter
import re
from dash_leaflet import GeoJSON
from dash_leaflet.express import dicts_to_geojson


def create_bike_markers(bikes: list[dict], city_id: int) -> GeoJSON:
    """Create clustered geo json markers for bike locations in city.

    Args:
        bikes (list[dict]): bikes
        city_id (int): city id

    Returns:
        GeoJSON: bike markers
    """
    bikes = [
        {"lat": b["lat"], "lon": b["lng"]} for b in bikes if b["city_id"] == city_id
    ]
    child = GeoJSON(
        data=dicts_to_geojson(bikes),
        cluster=True,
        superClusterOptions={"radius": 100},
    )
    return child


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
