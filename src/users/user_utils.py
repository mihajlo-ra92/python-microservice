from functools import wraps
import json
from logging import Logger
from logging.config import dictConfig
import os

from flask import Flask, request
from flask_mysqldb import MySQL
import jwt

from user_model import UserData
from user_service import UserService

SECRET_KEY = os.environ.get("SECRET_KEY")
# SECRET_KEY = "37de7552-b2e9-11ed-875c-45eb8b791582"


def init_app() -> Flask:
    app = Flask(__name__)
    app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
    return app


def set_start() -> tuple[Flask, MySQL, Logger, UserService]:
    app: Flask = init_app()
    mysql = MySQL(app)
    logger = app.logger
    service = UserService(mysql, logger)
    return [app, mysql, logger, service]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Bearer")
        if not token:
            return json.dumps({"text": "Token is missing"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as inst:
            return json.dumps({"text": "Token is missing or invalid"}), 401
        user_data = UserData(data["user"], data["user_type"])
        return f(user_data, *args, **kwargs)

    return decorated


def set_logger_config():
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )
