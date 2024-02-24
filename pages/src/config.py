"""Configuration"""

import os

# General
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
APP_NAME = "Bike Radar"
DB_NAME = "bikeradar.db"
DB_TABLE = "bikes"
CLAIM = "Book your nearby Nextbike ride the moment it appears!"
DESCRIPTION = f"""{APP_NAME} is a free and open source app for Nextbike users.
It secures nearby rides for you by booking them as soon as they
become available in your selected area."""
GITHUB_REPO_URL = "https://github.com/mc51/bike-radar"
MAX_BIKES = 3
BOOKING_TIME_FORMAT = r"%H:%M"

# Map
MIN_RADAR_RADIUS = 100
MAX_RADAR_RADIUS = 1000
DEFAULT_RADAR_RADIUS = 500
RADAR_RADIUS_STEP = 250
FRONTEND_REFRESH_INTERVAL = 1000 * 15  # in ms
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


# Meta tags
METATAGS = {
    "description": DESCRIPTION,
    "og:image": "/assets/logo.png",
    "smartbanner:title": "Bike Radar for Nextbike",
    "smartbanner:author": "www.data-dive.com",
    "smartbanner:price": "FREE",
    "smartbanner:price-suffix-google": " - In Google Play",
    "smartbanner:icon-google": "http://lh3.ggpht.com/f4oX61ljZ6x8aYDELZOgxlvdUEu73-wSQ4fy5bx6fCRISnZP8T353wdaM43RO_DbGg=w300",
    "smartbanner:button": "VIEW",
    "smartbanner:button-url-google": "https://play.google.com/store/apps/details?id=com.data_dive.com.bikeradar",
    "smartbanner:enabled-platforms": "android",
    "smartbanner:close-label": "Close",
    "smartbanner:hide-ttl": "1000",
}

META_TAGS = [{"name": k, "content": v} for k, v in METATAGS.items()]
