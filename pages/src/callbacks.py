"""Callbacks"""
import logging

import dash_bootstrap_components as dbc
from dash import Input, Output, Patch, State, get_app, no_update
from dash._callback import NoUpdate
from dash_leaflet import Map
from requests import HTTPError

from pages.src import config
from pages.src.api import Api
from pages.src.layout import Layout
from pages.src.locations import Locations

log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)


class Callbacks:
    """Callbacks class"""

    DEBUG = config.DEBUG
    MIN_RADAR_RADIUS = config.MIN_RADAR_RADIUS
    MAX_RADAR_RADIUS = config.MAX_RADAR_RADIUS
    DEFAULT_RADAR_RADIUS = config.DEFAULT_RADAR_RADIUS
    RADAR_RADIUS_STEP = config.RADAR_RADIUS_STEP
    REFRESH_INTERVAL = config.FRONTEND_REFRESH_INTERVAL
    STATUS_MSG_DURATION = config.STATUS_MSG_DURATION

    def __init__(self):
        log.debug("callbacks")
        self.app = get_app()
        self.api = Api()

    def register_callbacks(self) -> None:
        """Register callbacks."""

        self.app.callback(
            Output("store", "data", allow_duplicate=True),
            Output("login_feedback", "children"),
            Output("login_feedback", "color"),
            Output("login_feedback", "is_open"),
            Output("radar_control_div", "hidden"),
            Output("login_div", "hidden"),
            Input("login_button", "n_clicks"),
            State("phone", "value"),
            State("pin", "value"),
            prevent_initial_call=True,
        )(self.cb_check_login)

        self.app.callback(
            Output("store", "data", allow_duplicate=True),
            Output("map_div", "children"),
            Output("city_select_div", "hidden"),
            Output("login_div", "hidden", allow_duplicate=True),
            Input("city_select_button", "n_clicks"),
            State("city_select_dropdown", "value"),
            prevent_initial_call=True,
        )(self.cb_select_city)

        self.app.callback(
            Output("store", "data", allow_duplicate=True),
            Output("radar_circle", "radius"),
            Input("radar_slider", "value"),
            State("store", "data"),
            prevent_initial_call=True,
        )(self.cb_set_radar_radius)

        self.app.callback(
            Output("store", "data", allow_duplicate=True),
            Output("radar_circle", "center"),
            Input("map", "coords"),
            State("store", "data"),
            prevent_initial_call=True,
        )(self.cb_set_radar_position)

        self.app.callback(
            Output("store", "data", allow_duplicate=True),
            Output("booking_status_2", "children", allow_duplicate=True),
            Output("interval", "disabled", allow_duplicate=True),
            Input("interval", "n_intervals"),
            State("store", "data"),
            prevent_initial_call=True,
        )(self.cb_interval_triggered)

        self.app.callback(
            output=[
                Output("store", "data", allow_duplicate=True),
                Output("booking_status_1", "children", allow_duplicate=True),
                Output("booking_status_2", "children", allow_duplicate=True),
                Output("booking_button", "children"),
                Output("booking_button", "color"),
                Output("booking_spinner", "spinner_style"),
                Output("interval", "disabled"),
            ],
            inputs=[
                Input("booking_button", "n_clicks"),
                State("store", "data"),
            ],
            prevent_initial_call=True,
        )(self.toggle_auto_booking)

    def cb_select_city(self, _, city: str) -> tuple[dict, Map, bool, bool]:
        """Select city to show on map. Display login after selection.

        Args:
            city (str): city name

        Returns:
            tuple[dict, Map, bool, bool]:
                store data,
                map div children,
                city_select_div hidden,
                login_div hidden
        """
        locations = Locations()
        selected_city = locations.get_city_from_name(city)
        store_data = {
            "lat": selected_city["lat"],
            "lon": selected_city["lng"],
            "zoom": selected_city["zoom"],
            "city_id": selected_city["uid"],
            "radius": self.DEFAULT_RADAR_RADIUS,
        }
        log.info("Selected: %s", store_data)
        return store_data, Layout().create_map_layout(**store_data), True, False

    def cb_check_login(
        self, _, phone: str, pin: int
    ) -> tuple[Patch | NoUpdate, str, str, bool, bool, bool]:
        """Check login credentials. Display radar controls after successful
        login and save loginkey to store data.

        Args:
            phone (str): phone number
            pin (int): pin

        Returns:
            tuple[Patch | NoUpdate, str, str,  bool, bool, bool]:
                store data,
                alert text, alert color, alert is_open,
                radar div hidden, login div hidden
        """
        log.info("Checking login credentials.")
        if not phone or not pin:
            return (
                no_update,
                "Please enter your Nextbike phone and PIN.",
                "danger",
                True,
                True,
                False,
            )
        login_key = self.api.authenticate(phone, pin)
        if not login_key:
            return (
                no_update,
                "Login failed. Please check credentials and retry.",
                "danger",
                True,
                True,
                False,
            )
        store_data = Patch()
        store_data["login_key"] = login_key  # update single value
        return (
            store_data,
            "Login successful.",
            "success",
            True,
            False,
            True,
        )

    def cb_set_radar_radius(self, value: int, store_data: dict) -> tuple[dict, int]:
        """Change radar radius according to slider settings.

        Args:
            value (int): slider value

        Returns:
            tuple[dict, dict]: status, radius
        """
        log.debug("Radar radius from slider %s", value)
        if not store_data:
            log.warning("no store_data")
            store_data = {
                "booked": False,
            }
        store_data["radius"] = value
        log.debug("Setting radius. Status %s", store_data)
        return store_data, store_data["radius"]

    def cb_set_radar_position(
        self, coords: list, store_data: dict
    ) -> tuple[dict | NoUpdate, list | NoUpdate]:
        """Set radar position and save coordinates from click on map.

        Args:
            coords (list): click coordinates
            store_data (dict): store data

        Returns:
            tuple[dict | NoUpdate, list | NoUpdate]: store data, center coordinates
        """
        log.debug(coords)
        if not store_data:
            log.warning("no store_data")
            store_data = {
                "radius": self.DEFAULT_RADAR_RADIUS,
                "booked": False,
            }
        if not coords:
            # Bc we create the Map object dynamically, this will be triggered
            # catch that case without failing
            log.info("No coord set yet.")
            return no_update, no_update

        store_data["lat"] = round(coords[0], 5)
        store_data["lon"] = round(coords[1], 5)
        store_data["center"] = [store_data["lat"], store_data["lon"]]
        log.debug("Setting position. Status %s", store_data)
        return store_data, store_data["center"]

    def toggle_auto_booking(
        self, n_clicks: int, store_data: dict
    ) -> tuple[
        dict | NoUpdate,
        dbc.Alert,
        str | NoUpdate,
        str | NoUpdate,
        str | NoUpdate,
        dict | NoUpdate,
        bool | NoUpdate,
    ]:
        """Enable auto booking. Triggered regularly.

        Args:
            n_clicks (int): interval number
            store_data (dict): store data

        Returns:
            tuple[dict | NoUpdate,
                dbc.Alert, str | NoUpdate,
                str | NoUpdate, str | NoUpdate,
                dict | NoUpdate,
                bool | NoUpdate]:
            store data,
            booking status 1 children, booking status 2 children,
            booking button children, color,
            booking_spinner style, disable interval
        """
        log.info("Enable auto booking button triggered %s", n_clicks)
        log.debug(store_data)
        if not store_data or not store_data.get("lat"):
            log.info("Not set store_data yet")
            return (
                no_update,
                dbc.Alert(
                    "You need to set a location first",
                    color="danger",
                    duration=self.STATUS_MSG_DURATION,
                ),
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            )
        if store_data.get("enabled"):
            # is enabled, so toggle off
            store_data["enabled"] = False
            return (
                store_data,
                dbc.Alert(
                    "Auto booking disabled",
                    color="success",
                    duration=self.STATUS_MSG_DURATION,
                ),
                no_update,
                "Enable auto booking",
                "success",
                {"opacity": 0},  # hide spinner
                True,
            )
        # is disabled, so toggle on
        store_data["enabled"] = True
        return (
            store_data,
            dbc.Alert(
                "Auto booking enabled",
                color="success",
                duration=self.STATUS_MSG_DURATION,
            ),
            "Status: Please wait. Retrieving current status",
            "Disable auto booking",
            "danger",
            {"opacity": 1},  # show spinner
            False,
        )

    def cb_interval_triggered(
        self, n_intervals: int, store_data: dict
    ) -> tuple[dict | NoUpdate, str | NoUpdate, bool | NoUpdate]:
        """Interval triggered.

        Args:
            n_intervals (int): interval number
            store_data (dict): store_data

        Returns:
            tuple[dict | NoUpdate, str | NoUpdate, bool | NoUpdate]:
            store_data,
            booking status 2,
            disable interval
        """
        log.info("Interval triggered %s", n_intervals)
        log.debug("store_data: %s", store_data)
        locations = Locations(store_data)
        try:
            booking = locations.start_booking_process()
        except HTTPError as e:
            log.exception(e)
            return no_update, f"Error booking bike: {e}", no_update
        if booking:
            store_data["booked"] = booking.is_active
            return store_data, booking.to_status(), no_update
        return no_update, no_update, no_update
