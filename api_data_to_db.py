"""Regularly get all data from api and store to db"""
from datetime import datetime, timezone
import json
import logging
import sqlite3
import time

import requests
from pages.src import config


logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message).400s",
    force=True,
    level=logging.ERROR,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL)

CONNECTION = sqlite3.connect(config.DB_NAME)


def get_all_data() -> dict:
    """Get all data from API.

    Returns:
        dict: json data
    """
    params = {
        "api_key": config.API_KEY,
        "bikes": "0",
    }

    response = requests.get(
        config.MAPS_URL,
        params=params,
        headers=config.HEADERS,
        timeout=config.API_TIMEOUT,
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        log.error(err)
        log.error(response.text)
    log.debug("Response: %s", response.text)
    json_response = response.json()
    return json_response


def create_db_table(con: sqlite3.Connection):
    """Create db table of not exists yet.

    Args:
        con (sqlite3.Connection): connection
    """
    try:
        with con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS bikes
                        (
                            data TEXT,
                            created_at TEXT
                        )
                        """
            )
    except sqlite3.Error:
        log.exception("DB Error creating table.")
    else:
        log.info("DB created")


def write_data_to_db(con: sqlite3.Connection, json_data: dict):
    """Write data to db.

    Args:
        con (sqlite3.Connection): connection
        data (dict): json data
    """
    now = datetime.now(tz=timezone.utc)
    data = json.dumps(json_data)
    try:
        with con:
            con.execute(
                "INSERT INTO bikes(data, created_at) VALUES(?, ?)",
                (data, now),
            )
    except sqlite3.Error:
        log.exception("DB Error writing data.")
    else:
        log.info("DB updated")


def update_loop(con: sqlite3.Connection):
    """Update db with API data.

    Args:
        con (sqlite3.Connection): _description_
    """
    log.info("Start update loop")
    while True:
        data = get_all_data()
        write_data_to_db(con, data)
        time.sleep(config.REFRESH_INTERVAL)


def main():
    """Main"""
    log.info("Start get_data.py")
    create_db_table(CONNECTION)
    update_loop(CONNECTION)
    log.info("End get_data.py")


if __name__ == "__main__":
    main()
