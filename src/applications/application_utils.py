from datetime import datetime
from enum import Enum
from functools import wraps
import json, os, jwt
from logging import Logger
from logging.config import dictConfig
from flask import Flask, request
from flask_mysqldb import MySQL
from application_model import Application, UserData, ApplicationDecision
from application_service import ApplicationService

SECRET_KEY = os.environ.get("SECRET_KEY")


def init_app() -> Flask:
    app = Flask(__name__)
    app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
    if os.environ.get("TEST") == "TRUE":
        app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB_APPLICATIONS") + "_test"
    else:
        app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB_APPLICATIONS")
    return app


def set_start() -> tuple[Flask, MySQL, Logger, ApplicationService]:
    app: Flask = init_app()
    mysql = MySQL(app)
    logger = app.logger
    service = ApplicationService(mysql, logger)
    return [app, mysql, logger, service]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Bearer")
        if not token:
            return json.dumps({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as inst:
            return json.dumps({"message": "Token is invalid"}), 401
        user_data = UserData(data["username"], data["user_type"])
        return f(user_data, *args, **kwargs)

    return decorated


def read_jwt(token) -> UserData:
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return UserData(data["username"], data["user_type"])


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


def read_application(json: any) -> Application:
    application = Application()
    application.worker_id = json["worker_id"]
    application.job_id = json["job_id"]
    application.description = json["description"]
    return application


def read_decision(json: any) -> ApplicationDecision:
    decision: ApplicationDecision = None
    if json["decision"] == "ACCEPT":  # TODO: Update to use enum, not string
        decision = ApplicationDecision.ACCEPT
    if json["decision"] == "REJECT":  # TODO: Update to use enum, not string
        decision = ApplicationDecision.REJECT
    return decision


def serialize_job(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    return obj.__dict__
