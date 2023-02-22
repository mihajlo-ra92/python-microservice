import os, uuid, json
from typing import Optional, Union
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
    try:
        user_id = sent_user["id"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"text": "Please send id"}), 400
    user: Optional[User] = service.read_by_id(user_id)
    if user == None:
        return json.dumps({"text": "Invalid user_id"}), 400
    return json.dumps(user), 200


@server.route("/read-by-username", methods=["GET"])
def read_by_username():
    try:
        username = request.json["username"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"text": "Please send username"}), 400
    user: User = service.read_by_username(username)
    if user == None:
        return json.dumps({"text": "Invalid username"}), 400
    return json.dumps(user), 200


@server.route("/create-user", methods=["POST"])
def create():
    # TODO: check request.json, if invalid send bad request
    sent_user: User = request.json
    created_user: User = service.create(sent_user)
    return created_user, 201


@server.route("/update-user", methods=["PUT"])
def update():
    # TODO: check request.json, if invalid send bad request
    sent_user: User = request.json
    updated_user: User = service.update(sent_user)
    return updated_user, 200


@server.route("/delete-user", methods=["DELETE"])
def delete():
    # TODO: check request.json for id, if invalid send bad request
    sent_user: User = request.json
    deleted: bool = service.delete_by_id(sent_user["id"])
    return json.dumps(deleted), 200


@server.route("/check-info", methods=["GET"])
def check_info():
    logger.info(request.json)
    try:
        username, password = request.json["username"], request.json["password"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"text": "Please send username and password"}), 400
    jwt_data: Union[str, tuple[str, str]] = service.check_info(username, password)
    logger.info(jwt_data)
    if jwt_data == "Username invalid":
        return json.dumps({"text": jwt_data}), 401
    if jwt_data == "Password invalid":
        return json.dumps({"text": jwt_data}), 401
    return json.dumps({"username": jwt_data[0], "user_type": jwt_data[1]})


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
