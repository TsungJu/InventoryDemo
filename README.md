# InventoryDemo

[![CI to Docker Hub](https://github.com/TsungJu/InventoryDemo/actions/workflows/main.yml/badge.svg)](https://github.com/TsungJu/InventoryDemo/actions/workflows/main.yml)

[![Build and deploy Python app to Azure Web App - leoinventorydemo](https://github.com/TsungJu/inventory-demo/actions/workflows/master_leoinventorydemo.yml/badge.svg?branch=master)](https://github.com/TsungJu/inventory-demo/actions/workflows/master_leoinventorydemo.yml)

This is inventory analyze and management System build by flask and bootstrap.

## Prerequisites

### Create docker network:

$ `docker network create inventory-network`

### Run postgresql locally:

$ `docker run -d --name postgres-dev --network inventory-network -e POSTGRES_PASSWORD=33c15fbd604ee23e55421bb0dae653b769e3b1222765f51ce018690bb56b3539 -e POSTGRES_USER=qdmzygkpespeaf -e POSTGRES_DB=d87gbe1ta420fb -p 5432:5432 postgres`

## Build and run me

Modify `app/__init__.py` variable `config_name` to `development`

Linux:

$ `pip install -r requirements.txt`

$ `export FLASK_ENV=development`

$ `export FLASK_APP=app.webapp`

$ `flask run`

## Build and run me by docker

$ `docker build -t inventorydemo-web-docker-env .`

$ `docker run -it --rm -p 5000:5000 --name inventorydemo-web --network inventory-network -v %cd%:/opt/app -w /opt/app -e FLASK_APP=app.webapp inventorydemo-web-docker-env`

## Build and run me by docker-compose

$ `docker-compose up -d --build`