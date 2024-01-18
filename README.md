# Bike-Radar

[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json)](https://rye-up.com)

Bike Radar is a free and open source web app for Nextbike users. It secures nearby rides for you by booking them as soon as they become available in your selected area.

## Usage

Publicly hosted instance: [https://bikeradar.cc](https://bikeradar.cc)

You can host your own instance. For that, it's recommended to use [gunicorn](https://gunicorn.org/) behind a reverse proxy and add `run.sh` to a process control system (e.g. systemd, supervisor, etc.).

## Tech stack

* App built with [Dash](https://github.com/plotly/dash), map powered by  [dash-leaflet](https://www.dash-leaflet.com/)
* Served via [Gunicorn](https://gunicorn.org/)
* [Caddy](https://github.com/caddyserver/caddy) as reverse proxy
* [Supervisord](http://supervisord.org/) as process control service
  
