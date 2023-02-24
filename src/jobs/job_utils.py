import os, json, jwt
from functools import wraps
from logging import Logger
from logging.config import dictConfig
from flask import Flask, request
from flask_mysqldb import MySQL

SECRET_KEY = os.environ.get("SECRET_KEY")


def init_app() -> Flask:
    app = Flask(__name__)
    app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
    if os.environ.get("TEST") == "TRUE":
        app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB") + "_test"
    else:
        app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
    return app


def set_start() -> tuple[Flask, MySQL, Logger, JobsService]:
    app: Flask = init_app()
    mysql = MySQL(app)
    logger = app.logger
    service = UserService(mysql, logger)
    return [app, mysql, logger, service]
