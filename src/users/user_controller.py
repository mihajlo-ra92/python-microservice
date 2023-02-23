import json
import os
from typing import Optional, Union
from flask import request
from user_model import User, UserData

from user_utils import read_jwt, read_user, set_logger_config, set_start, token_required


set_logger_config()
[app, mysql, logger, service] = set_start()


@app.route("/read-users", methods=["GET"])
def read_all():
    logger.info("!!! DATABASE: !!!")
    logger.info(app.config["MYSQL_DB"])
    users: list[User] = service.read_all()
    return json.dumps(users), 200


@app.route("/read-by-id", methods=["GET"])
def read_by_id():
    sent_user = request.json
    try:
        user_id = sent_user["id"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send id"}), 400
    user: Optional[User] = service.read_by_id(user_id)
    if user == None:
        return json.dumps({"message": "Invalid user_id"}), 400
    return json.dumps(user), 200


# NOTE: Reads by username in jwt
@app.route("/read-logged-user", methods=["GET"])
@token_required
def read_logged_user(user_data):
    logged_user: UserData = user_data
    username = logged_user.username
    user: User = service.read_logged_user(username)
    if user == None:
        return json.dumps({"message": "Invalid username"}), 400
    return json.dumps(user), 200


@app.route("/read-by-username", methods=["GET"])
def read_by_username():
    try:
        username = request.json["username"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send username"}), 400
    user: User = service.read_by_username(username)
    if user == None:
        return json.dumps({"message": "Invalid username"}), 400
    return json.dumps(user), 200


@app.route("/create-user", methods=["POST"])
def create():
    try:
        sent_user: User = read_user(request.json)
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send all user data"}), 400
    created_user: User = service.create(sent_user)
    return created_user.toJSON(), 201


@app.route("/update-user", methods=["PUT"])
@token_required
def update():
    # TODO: Check if logged in user is the one being updated
    try:
        sent_user: User = read_user(request.json)
        sent_user.id = request.json["id"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send all user data"}), 400
    updated_user: User = service.update(sent_user)
    return updated_user, 200


@app.route("/delete-user", methods=["DELETE"])
@token_required
def delete(user_data):
    # TODO: check request.json for id, if invalid send bad request
    sent_user: User = request.json
    deleted: bool = service.delete_by_id(sent_user["id"])
    return json.dumps(deleted), 200


@app.route("/check-info", methods=["GET"])
def check_info():
    try:
        username, password = request.json["username"], request.json["password"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send username and password"}), 400
    jwt_data: Union[str, tuple[str, str]] = service.check_info(username, password)
    logger.info(jwt_data)
    if jwt_data == "Username invalid":
        return json.dumps({"message": jwt_data}), 401
    if jwt_data == "Password invalid":
        return json.dumps({"message": jwt_data}), 401
    return json.dumps({"username": jwt_data[0], "user_type": jwt_data[1]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
