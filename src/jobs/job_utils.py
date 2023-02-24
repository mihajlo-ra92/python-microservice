import os, json, jwt
from functools import wraps
from logging import Logger
from logging.config import dictConfig
from flask import Flask, request
from flask_mysqldb import MySQL

from job_service import JobService
from job_model import Job

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


def set_start() -> tuple[Flask, MySQL, Logger, JobService]:
    app: Flask = init_app()
    mysql = MySQL(app)
    logger = app.logger
    service = JobService(mysql, logger)
    return [app, mysql, logger, service]


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


def read_job(json: any) -> Job:
    job = Job()
    job.employer_id = json["employer_id"]
    job.worker_id = json["worker_id"]
    job.job_name = json["job_name"]
    job.job_desc = json["job_desc"]
    job.pay_in_euro = json["pay_in_euro"]
    job.completed = json["completed"]
    try:
        job.id = json["id"]
    except Exception:
        job.id = ""
    return job
