import os, uuid, json
from flask import Flask, request
from flask_mysqldb import MySQL
from user_service import UserService
from user_model import User
from logging.config import dictConfig


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

server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

mysql = MySQL(server)
service = UserService(mysql, server.logger)
logger = server.logger


@server.route("/read-users", methods=["GET"])
def read_all():
    logger.info("!!! FROM CONTROLLER !!!")
    users: list[User] = service.read_all()
    return json.dumps(users), 200


@server.route("/read-by-id", methods=["GET"])
def read_by_id():
    sent_user = request.json
    user_id = sent_user["id"]
    user: User = service.read_by_id(user_id)
    return json.dumps(user), 200


@server.route("/read-by-username", methods=["GET"])
def read_by_username():
    sent_user = request.json
    username = sent_user["username"]
    user: User = service.read_by_username(username)
    return json.dumps(user), 200


@server.route("/create-user", methods=["POST"])
def create():
    sent_user: User = request.json
    created_user: User = service.create(sent_user)
    return created_user, 201


@server.route("/update-user", methods=["PUT"])
def update():
    sent_user: User = request.json
    updated_user: User = service.update(sent_user)
    return updated_user, 200


@server.route("/delete-user", methods=["DELETE"])
def delete():
    sent_user: User = request.json
    deleted: bool = service.delete_by_id(sent_user["id"])
    return json.dumps(deleted), 200


@server.route("/check-info", methods=["GET"])
def check_info():
    logger.info(request.json)
    return json.dumps(request.json), 200
    username, password = request.json["username", "password"]
    valid: bool = service.check_info(username, password)
    return "HELLO !!!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
