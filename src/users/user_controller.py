import os, uuid, json
from flask import Flask, request
from flask_mysqldb import MySQL
from user_service import UserService

server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

mysql = MySQL(server)
service = UserService(mysql)


@server.route("/read-users", methods=["GET"])
def read_users():
    users = service.read_all()
    return json.dumps(users)


@server.route("/read-user", methods=["GET"])
def read_user():
    sent_user = request.json
    user_id = sent_user["id"]
    user = service.read_user(user_id)
    return json.dumps(user)


@server.route("/create-user", methods=["POST"])
def create_user():
    user = request.json
    username = user["username"]
    password = user["password"]
    email = user["email"]
    user_type = user["userType"]

    cur = mysql.connection.cursor()
    cur.execute(
        f"INSERT INTO Users(id, username, password, email, user_type) VALUES \
        ('{str(uuid.uuid1())}', '{username}', '{password}', '{email}', '{user_type}');"
    )
    mysql.connection.commit()
    cur.close()
    return json.dumps(user)


@server.route("/update-user", methods=["PUT"])
def update_user():
    user = request.json
    user_id = user["id"]
    username = user["username"]
    password = user["password"]
    email = user["email"]
    cur = mysql.connection.cursor()
    cur.execute(
        f"UPDATE  Users \
                SET username = '{username}', password = '{password}', email = '{email}' \
                WHERE id = '{user_id}';"
    )
    mysql.connection.commit()
    cur.close()
    return json.dumps(user)


@server.route("/delete-user", methods=["DELETE"])
def delete_user():
    user = request.json
    user_id = user["id"]
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Users WHERE id='{user_id}';")
    mysql.connection.commit()
    cur.close()
    return json.dumps(user)


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
