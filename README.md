# InventoryDemo

[![CI to Docker Hub](https://github.com/TsungJu/InventoryDemo/actions/workflows/main.yml/badge.svg)](https://github.com/TsungJu/InventoryDemo/actions/workflows/main.yml)

This is inventory management and analyze System build by flask and bootstrap.

## Prerequisites

### Run postgresql locally:

$ `docker run -d --name postgresql-dev -e POSTGRES_PASSWORD=33c15fbd604ee23e55421bb0dae653b769e3b1222765f51ce018690bb56b3539 -e POSTGRES_USER=qdmzygkpespeaf -e POSTGRES_DB=d87gbe1ta420fb -p 5432:5432 postgres`

## Build and run me

Modify `app/__init__.py` variable `config_name` to `development`

Linux:

$ `pip install -r requirements.txt`

$ `export FLASK_ENV=development`

$ `export FLASK_APP=app.webapp`

$ `flask run`

## Build and run me by docker

$ `docker build -t inventorydemo_web_docker_env .`

$ `docker run -it --rm -p 5000:5000 --name inventorydemo_web -v %cd%:/opt/app -w /opt/app -e FLASK_APP=app.webapp inventorydemo_web_docker_env`

## Build and run me by docker-compose

$ `docker-compose up -d --build`