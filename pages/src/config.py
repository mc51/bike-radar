"""Configuration"""
import os

# General
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
APP_NAME = "Bike Radar"
DB_NAME = "bikeradar.db"
DB_TABLE = "bikes"
CLAIM = "Book your nearby Nextbike ride the moment it appears!"
DESCRIPTION = f"""{APP_NAME} is a free and open source web app for Nextbike users.
It secures nearby rides for you by booking them as soon as they
become available in your selected area."""
GITHUB_REPO_URL = "https://github.com/mc51/bike-radar"
MAX_BIKES = 3
BOOKING_TIME_FORMAT = r"%H:%M"

# Map
MIN_RADAR_RADIUS = 100
MAX_RADAR_RADIUS = 1000
DEFAULT_RADAR_RADIUS = 800
RADAR_RADIUS_STEP = 250
FRONTEND_REFRESH_INTERVAL = 1000 * 30  # in ms
STATUS_MSG_DURATION = 1000 * 4  # in ms
MAX_BOOKING_DURATION_MIN = 20

# API
API_KEY = "rXXqTgQZUPZ89lzB"
API_TIMEOUT = 20
API_REFRESH_INTERVAL = 10
BASE_URL = "https://api.nextbike.net/api/v1.1/"
LOGIN_URL = BASE_URL + "login.json"
BOOKING_URL = BASE_URL + "booking.json"
BOOKINGS_URL = BASE_URL + "bookings.json"
BOOKING_INFO_URL = BASE_URL + "bookingInfo.json"
CANCEL_BOOKING_URL = BASE_URL + "cancelBooking.json"
# flatjson returned less nested data
MAPS_URL = "https://maps.nextbike.net/maps/nextbike-live.flatjson"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Gecko/20100101 Firefox/119.0",
}
