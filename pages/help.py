"""Help page"""
import dash
from dash import html
from pages.src.config import GITHUB_REPO_URL, APP_NAME


dash.register_page(__name__, title=f"{APP_NAME} - Help")

layout = html.Div(
    [
        html.P(
            """The app is currently still under heavy development.
            There is no warranty, so it might become unavailable at any time.
            If that happens, just try again later. Reliability is increasing
            fast and new features are constantly added. If you find bugs or
            want to suggest improvements, please reach out via mail.
            However, please take into account that the app doesn't strive to
            completely replace the Nextbike app but rather complement it.
            So, don't expect that all functions will be added any time soon.
            """
        ),
        html.Br(),
        html.H2("""Known limitations"""),
        html.Li("App can be slow, especially on mobile devices"),
        html.Li('Only "free floating" bikes are supported'),
        html.Li("Bookings cannot be canceled"),
        html.Li("Location of booked bike is not displayed on map"),
        html.Li(
            "If your provider, location or account type don't support booking "
            "(reserving) bikes, you'll receive errors or it simply won't work"
        ),
        html.Br(),
        html.H2("""Planned features"""),
        html.Li("Improve server and client side speed"),
        html.Li("Support bike stations"),
        html.Li("Show location of booked bike on map"),
        html.Br(),
        html.A("Find the source code here", href=GITHUB_REPO_URL),
        html.Br(),
        html.A(
            "Contact me",
            className="mail",
            href="javascript:window.location.href=atob('bWFpbHRvOmJpa2VyYWRhckBkYXRhLWRpdmUuY29tCg==')",
        ),
    ]
)
