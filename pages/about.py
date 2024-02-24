"""Radar page"""

import dash
from dash import html

from pages.src.config import (
    DESCRIPTION,
    GITHUB_REPO_URL,
    APP_NAME,
    MAX_BOOKING_DURATION_MIN,
    CLAIM,
)

dash.register_page(
    __name__, title=f"{APP_NAME} — {CLAIM} — About", description=DESCRIPTION
)

layout = html.Div(
    [
        html.H5(DESCRIPTION),
        html.Br(),
        html.H2("How to get started?"),
        html.P(
            """To get started, select your city and then login to your
            Nextbike account (use same credentials as in the Nextbike App).
            Following, set a location by clicking on the map and adjust the
            radius of the area in which to look for bikes.
            Finally, enable the auto booking feature to activate the
            radar. Don't navigate away or refresh the site, as this will
            log you out. However, to select a new city, just refresh the site
            and login again."""
        ),
        html.Br(),
        html.H2("What does auto booking do?"),
        html.P(
            f"""With auto booking enabled the nearest bike in your
            search area will be automatically booked. If none is readily
            available, the radar will continue to look for bikes.
            As soon as a bike in your area becomes available it will be booked.
            If a nearer bike become available while auto booking is active,
            it will be booked instead. Auto booking is automatically disabled
            after {MAX_BOOKING_DURATION_MIN} minutes to avoid misuse. You
            can turn it back on to keep looking for bikes."""
        ),
        html.Br(),
        html.H2("What to do after a booking?"),
        html.P(
            f"""A booking from {APP_NAME} will become visible in your Nextbike
            App as well. Use the Nextbike app to cancel it or navigate to your
            booked bike in order to rent it.
            Turn off the auto booking feature after a bike has been booked for
            you that you want to rent, so no other (closer) bike will be booked
            in the meantime. Your booking remains active until it expires or
            your rent the bike.
            """
        ),
        html.Br(),
        html.H2("""How does it work?"""),
        html.P(
            """For technical details and the source code, check out the GitHub
            repo linked below.
            """
        ),
        html.Br(),
        html.H2("""What does it cost?"""),
        html.P(
            f"""{APP_NAME} is completely free. However, depending on your Nextbike
            provider, location and your account type, booking of bikes might
            cost you. Make sure to check the pricing in your Nextbike App."""
        ),
        html.Br(),
        html.H2("""What about data safety?"""),
        html.P(
            f"""Data safety is taken seriously:
            The website does not use any cookies or tracking.
            {APP_NAME} does not store any personal data or credentials on the
            server. As the app is open source, you can check compliance
            yourself or even run your own instance of it.
            """
        ),
        html.A("Find the source code here", href=GITHUB_REPO_URL),
        html.Br(),
        html.A(
            "Contact me",
            className="mail",
            href="javascript:window.location.href=atob('bWFpbHRvOmJpa2VyYWRhckBkYXRhLWRpdmUuY29tCg==')",
        ),
    ]
)
