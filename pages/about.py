"""Radar page"""
import dash
from dash import html

from pages.bike_radar.config import DESCRIPTION, GITHUB_REPO_URL, APP_NAME


dash.register_page(__name__, title=f"{APP_NAME} - About", description=DESCRIPTION)


layout = html.Div(
    [
        html.H5(DESCRIPTION),
        html.Br(),
        html.H2("""How to use?"""),
        html.P(
            """To get started, select the city you want to book a bike in.
            Then, login to your Nextbike account (use same credentials as in
            the Nextbike App). Following, set your desired location by clicking
            on the map and adjust the radius of the area in which to look for
            bikes. Finally, enable the auto booking feature to activate the
            radar."""
        ),
        html.P(
            """As soon as a bike in your area becomes available it will
            automatically be booked.
            The distance to the bike, its identifier and the duration of your
            booking will be displayed in the status.
            If a nearer bike become available in the meantime, your booking
            will be changed.
            """
        ),
        html.P(
            """A booking will become visible in your Nextbike App as well.
            Use the app to cancel it or navigate to your booked bike in order
            to rent it. Turn off the auto booking feature after a bike has been
            booked for you. Your booking remains active until it expires or
            your rent the bike.
            """
        ),
        html.Br(),
        html.H2("""How does it work?"""),
        html.P(
            f"""{APP_NAME} is using the API of the Nextbike app to take
            automatic actions for you. It regularly refreshes the location of
            nearby bikes and looks for them within the set search area.
            If bikes become available within the search area, the closest one
            will automatically be booked (i.e. reserved, but not rented).
            For technical details and the source code, check out the GitHub
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
