# InventoryDemo

[![CI to Docker Hub](https://github.com/TsungJu/InventoryDemo/actions/workflows/main.yml/badge.svg)](https://github.com/TsungJu/InventoryDemo/actions/workflows/main.yml)

This is inventory management and analyze System build by python and Jinja.

[ Prerequisites ]

Run postgresql locally:

$ `docker run -d --name postgresql-dev -e POSTGRES_PASSWORD=33c15fbd604ee23e55421bb0dae653b769e3b1222765f51ce018690bb56b3539 -e POSTGRES_USER=qdmzygkpespeaf -e POSTGRES_DB=d87gbe1ta420fb -p 5432:5432 postgres`

[ Build and run me ]

Modify `app/__init__.py` variable `config_name` to `development`

Linux:

$ `pip install -r requirements.txt`

$ `export FLASK_ENV=development`

$ `export FLASK_APP=app.webapp`

$ `flask run`
