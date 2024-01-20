# %%
"""App Frontend layout and functionality"""
import logging

import dash_bootstrap_components as dbc
import dash_leaflet
from dash import dcc, html
from dash_extensions.javascript import assign
from dash_leaflet import LayerGroup, Map, TileLayer

from pages.src import config
from pages.src.locations import Locations
from pages.src.utils import create_bike_markers

log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)


class Layout:
    """Layout class."""

    DEBUG = config.DEBUG
    MIN_RADAR_RADIUS = config.MIN_RADAR_RADIUS
    MAX_RADAR_RADIUS = config.MAX_RADAR_RADIUS
    DEFAULT_RADAR_RADIUS = config.DEFAULT_RADAR_RADIUS
    RADAR_RADIUS_STEP = config.RADAR_RADIUS_STEP
    REFRESH_INTERVAL = config.FRONTEND_REFRESH_INTERVAL
    STATUS_MSG_DURATION = config.STATUS_MSG_DURATION

    MAP_CLICK_HANDLER = {
        "click": assign(
            """function(e, ctx){
                        ctx.setProps({ coords: [e.latlng['lat'], e.latlng['lng']] })
            }"""
        )
    }

    def __init__(self):
        log.debug("layout")
        self.locations = Locations()

    def create_page_layout(self) -> html.Div:
        """Create page layout.

        Returns:
            html.Div: layout
        """
        return html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="/assets/logo.png",
                            id="logo",
                            height="300vh",
                            hidden=False,
                            style={
                                "margin-left": "auto",
                                "margin-right": "auto",
                                "display": "block",
                            },
                        ),
                        html.Div(
                            self.create_city_select_layout(),
                            id="city_select_div",
                            hidden=False,
                        ),
                        html.Div(
                            self.create_login_layout(),
                            id="login_div",
                            hidden=True,
                        ),
                        dbc.Alert(
                            is_open=False,
                            id="login_feedback",
                            fade=True,
                            duration=4000,
                        ),
                        html.Br(),
                        html.Div(
                            self.create_radar_control_layout(),
                            id="radar_control_div",
                            hidden=True,  # only show after login
                        ),
                        html.Br(),
                        html.Div(id="booking_status_1"),
                        html.Div(id="booking_status_2"),
                        html.Div(id="booking_status_3"),
                        html.Br(),
                    ],
                ),
                html.Div(id="map_div"),
                dcc.Store(id="store", storage_type="memory"),
                dcc.Interval(
                    id="interval",
                    interval=self.REFRESH_INTERVAL,
                    disabled=True,
                ),
            ],
        )

    def create_city_select_layout(self) -> dbc.Form:
        """Create city select form layout.

        Returns:
            dbc.Form: form layout
        """
        cities = self.locations.get_city_names()
        form = dbc.Form(
            id="city_select_form",
            children=[
                dbc.Label("Where to look for bikes?", width="auto"),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                cities,
                                placeholder="Select city",
                                id="city_select_dropdown",
                                maxHeight=400,
                                clearable=False,
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Select", id="city_select_button", color="primary"
                            ),
                            width="auto",
                        ),
                    ],
                ),
            ],
        )
        return form

    def create_login_layout(self) -> dbc.Form:
        """Create login form layout.

        Returns:
            dbc.Form: form layout
        """
        form = dbc.Form(
            id="login_form",
            children=[
                dbc.Label("Login to Nextbike Account", width="auto"),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                type="string",
                                id="phone",
                                placeholder="Phone no.",
                            ),
                            width=6,
                        ),
                    ],
                    justify="start",
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="pin",
                                placeholder="PIN",
                            ),
                            width=6,
                        ),
                    ],
                    justify="start",
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Login", id="login_button", color="primary"),
                            width=2,
                        ),
                    ],
                    justify="start",
                ),
            ],
        )
        return form

    def create_radar_control_layout(self) -> dbc.Form:
        """Create radar control layout.

        Returns:
            dbc.Form: form layout
        """
        layout = dbc.Form(
            id="radar_control_form",
            children=[
                dbc.Label("Click on the map to set radar location", width="auto"),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Label("Set radius (m)", width="auto"),
                        dbc.Col(
                            dcc.Slider(
                                self.MIN_RADAR_RADIUS,
                                self.MAX_RADAR_RADIUS,
                                self.RADAR_RADIUS_STEP,
                                value=self.DEFAULT_RADAR_RADIUS,
                                id="radar_slider",
                            ),
                        ),
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                children="Enable auto booking",
                                id="booking_button",
                                color="success",
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Spinner(
                                id="booking_spinner",
                                color="primary",
                                spinner_style={"opacity": 0},  # hide on start
                            ),
                            width="auto",
                        ),
                    ],
                ),
            ],
        )
        return layout

    def create_map_layout(
        self, lat: float, lon: float, zoom: int, radius: int, city_id: int
    ) -> Map:
        """Create map layout for selected city.

        Args:
            lat (float): map center lat
            lon (float): map center lon
            zoom (int): map zoom
            radius (int): radar radius
            city_id (int): city id

        Returns:
            Map: map
        """
        layout = Map(
            children=[
                TileLayer(),
                dash_leaflet.Circle(
                    id="radar_circle",
                    center=[lat, lon],
                    radius=radius,
                    color="#ff6666",
                    fillOpacity=0.5,
                    stroke=False,
                ),
                LayerGroup(
                    children=create_bike_markers(
                        bikes=self.locations.bikes, city_id=city_id
                    ),
                    id="map_markers",
                ),
            ],
            eventHandlers=self.MAP_CLICK_HANDLER,
            style={"height": "50vh"},
            center=[lat, lon],
            zoom=zoom,
            id="map",
        )
        return layout
