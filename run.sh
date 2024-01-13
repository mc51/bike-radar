#!/bin/bash
.venv/bin/gunicorn app:server -w 2 -b localhost:5555
