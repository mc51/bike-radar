#!/bin/bash
exec .venv/bin/gunicorn app:server -w 2 -b localhost:5555
