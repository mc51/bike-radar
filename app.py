"""Main app"""
import logging

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

from pages.src.config import DEBUG, APP_NAME, DESCRIPTION
from pages.src.callbacks import Callbacks
from pages.src.utils import RedactingFormatter

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message).400s",
    force=True,
    level=logging.ERROR,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)
# hide any sensitive information even on debug level
for h in logging.root.handlers:
    h.setFormatter(RedactingFormatter(h.formatter))
log.setLevel(logging.DEBUG)

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.YETI],
    meta_tags=[{"name": "description", "content": DESCRIPTION}],
    serve_locally=DEBUG,  # In production use CDN to serve dash js and css
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
    className="mycontent",
    style={"height": "100%", "margin": "auto"},
)

Callbacks().register_callbacks()


def main():
    """Main"""
    app.run(debug=DEBUG)


if __name__ == "__main__":
    main()
