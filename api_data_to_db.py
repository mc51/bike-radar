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
                f"""CREATE TABLE IF NOT EXISTS {config.DB_TABLE}
                        (
                            data TEXT,
                            created_at TEXT
                        )
                        """
            )
    except sqlite3.Error:
        log.exception("ERROR: creating db table.")
        raise
    log.info("OK: created db table.")


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
            con.execute(f"DELETE FROM {config.DB_TABLE}")
            con.execute(
                f"INSERT INTO {config.DB_TABLE} (data, created_at) VALUES(?, ?)",
                (data, now),
            )
    except sqlite3.Error:
        log.exception("ERROR: writing data to db table.")
    else:
        log.info("OK: updated table data.")


def update_loop(con: sqlite3.Connection):
    """Update db with API data.

    Args:
        con (sqlite3.Connection): _description_
    """
    log.info("Start update loop")
    while True:
        data = get_all_data()
        write_data_to_db(con, data)
        time.sleep(config.API_REFRESH_INTERVAL)


def main():
    """Main"""
    log.info("Starting to get data from API and save to db.")
    create_db_table(CONNECTION)
    update_loop(CONNECTION)
    log.info("Finishing getting data.")


if __name__ == "__main__":
    main()
