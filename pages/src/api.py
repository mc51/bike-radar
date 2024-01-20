"""Api stuff"""
import logging

import requests

from pages.src import config

log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)


class Api:
    """Api class."""

    API_KEY = config.API_KEY
    API_TIMEOUT = config.API_TIMEOUT
    BASE_URL = config.BASE_URL
    LOGIN_URL = config.LOGIN_URL
    HEADERS = config.HEADERS
    MAPS_URL = config.MAPS_URL
    BOOKING_URL = config.BOOKING_URL
    BOOKINGS_URL = config.BOOKINGS_URL
    BOOKING_INFO_URL = config.BOOKING_INFO_URL
    CANCEL_BOOKING_URL = config.CANCEL_BOOKING_URL

    def __init__(self, login_key: str | None = None):
        self.mobile = None
        self.pin = None
        self.login_key = login_key

    def send_api_request(
        self, url: str, params: dict | None = None, post: bool = False
    ) -> dict:
        """Send request to api and return json results.

        Args:
            url (str): url
            params (dict, optional): parameters. Defaults to None.
            post (bool, optional): post request. Defaults to False.

        Returns:
            dict: response
        """
        log.debug("Sending request with params %s", params)

        if post:
            response = requests.post(
                url,
                json=params,
                headers=self.HEADERS,
                timeout=self.API_TIMEOUT,
            )
        else:
            response = requests.get(
                url,
                params=params,
                headers=self.HEADERS,
                timeout=self.API_TIMEOUT,
            )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log.error(err)
            log.error(response.text)
        log.debug("Response: %s", response.text)
        json_response = response.json()
        return json_response

    def authenticate(self, phone: str, pin: int) -> str | None:
        """Authenticate to api and save loginkey.
        Args:
            phone (str): phone number
            pin (int): pin

        Returns:
            str | None: login key
        """
        log.info("Authenticating to API and getting login key")
        payload = {
            "api_key": self.API_KEY,
            "mobile": phone,
            "pin": pin,
        }
        response = self.send_api_request(self.LOGIN_URL, payload, post=True)
        if response.get("error"):
            log.error("ERROR: Authentication failed %s", response["error"])
            return None
        log.info("OK: Authentication successful")
        self.login_key = response["user"]["loginkey"]
        return self.login_key

    def request_locations(self, city_id: int | None = None) -> dict[str, list]:
        """Request location data.

        Args:
            city (int | None, optional): Filter on city. Defaults to None.

        Returns:
            dict[str, list]: places
        """
        log.debug("Getting all locations. Filter on %s:", city_id)
        params = {
            "api_key": self.API_KEY,
            "bikes": "0",
            "city": city_id,
        }
        response = self.send_api_request(self.MAPS_URL, params)
        return response

    def request_booking_info(self, place_id: int) -> dict:
        """Request booking information on place.

        Args:
            place_id (int): place id

        Returns:
            dict: booking information
        """
        params = {
            "api_key": self.API_KEY,
            "loginkey": self.login_key,
            "place": place_id,
        }
        response = self.send_api_request(self.BOOKING_INFO_URL, params)
        return response

    def request_bike_booking(self, place_id: int) -> dict:
        """Request bike booking.

        Args:
            place_id (int): place id

        Returns:
            dict: booking result
        """
        params = {
            "api_key": self.API_KEY,
            "loginkey": self.login_key,
            "place": place_id,
            "num_bikes": 1,
        }
        response = self.send_api_request(self.BOOKING_URL, params)
        return response

    def request_booking_cancellation(self, booking_id: int) -> dict:
        """Request cancellation of bike booking.

        Args:
            booking_id (int): booking id

        Returns:
            dict: cancellation response
        """
        params = {
            "api_key": self.API_KEY,
            "loginkey": self.login_key,
            "booking_id": booking_id,
        }
        response = self.send_api_request(self.CANCEL_BOOKING_URL, params)
        return response

    def request_bookings(self) -> dict:
        """Request all bookings. Returns all past and present bookings with status
        and additional infos.

        Returns:
            dict: bookings
        """
        params = {
            "api_key": self.API_KEY,
            "loginkey": self.login_key,
        }
        response = self.send_api_request(self.BOOKINGS_URL, params)
        return response
