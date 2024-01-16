"""start page"""
import dash
from dash import html

from pages.src.layout import Layout
from pages.src.config import DESCRIPTION, APP_NAME, CLAIM

dash.register_page(
    __name__, path="/", title=f"{APP_NAME} - Home", description=DESCRIPTION
)

layout = html.Div(
    [
        html.H5(CLAIM),
        html.Br(),
        Layout().create_page_layout(),
    ]
)
