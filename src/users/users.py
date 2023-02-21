import os, uuid, json
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

mysql = MySQL(server)


@server.route("/users", methods=["GET"])
def get_users():
    cur = mysql.connection.cursor()
    _ = cur.execute(f"SELECT * FROM Users")
    user_details = cur.fetchall()
    cur.close()
    return json.dumps(user_details)


@server.route("/add-user", methods=["POST"])
def add_user():
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
    return "added user"


@server.route("/delete-user", methods=["DELETE"])
def delete_user():
    user = request.json
    user_id = user["id"]
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Users WHERE id='{user_id}';")
    mysql.connection.commit()
    cur.close()
    return "deleted user"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
