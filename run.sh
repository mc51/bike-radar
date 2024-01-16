#!/bin/bash
exec .venv/bin/python api_data_to_db.py &
exec .venv/bin/gunicorn app:server -w 4 -b localhost:5555
