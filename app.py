"""Main app"""
import logging

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

from pages.src.config import DEBUG, APP_NAME
from pages.src.callbacks import Callbacks

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message).2000s",
    force=True,
    level=logging.ERROR,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
app.layout = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(page["name"]),
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            pills=True,
            horizontal="center",
        ),
        html.Br(),
        html.H1(APP_NAME),
        html.Br(),
        dash.page_container,
        html.Br(),
    ],
    style={"height": "700px", "width": "900px", "margin": "auto"},
)

Callbacks().register_callbacks()


def main():
    """Main"""
    app.run(debug=DEBUG)


if __name__ == "__main__":
    main()
