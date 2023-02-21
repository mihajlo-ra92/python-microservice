import os, uuid, json
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

# TODO: read env_vars not  regular string
server.config["MYSQL_HOST"] = "mysql"
server.config["MYSQL_USER"] = "root"
server.config["MYSQL_PASSWORD"] = "password"
server.config["MYSQL_DB"] = "users"

mysql = MySQL(server)


@server.route("/users", methods=["GET"])
def index():
    cur = mysql.connection.cursor()
    _ = cur.execute(f"SELECT * FROM Users")
    user_details = cur.fetchall()
    cur.close()
    return json.dumps(user_details)


@server.route("/add-user", methods=["POST"])
def add_user():
    user_details = request.json
    username = user_details["username"]
    password = user_details["password"]
    email = user_details["email"]

    cur = mysql.connection.cursor()
    cur.execute(
        f"INSERT INTO Users(id, username, password, email) VALUES \
        ('{str(uuid.uuid1())}', '{username}', '{password}', '{email}');"
    )
    mysql.connection.commit()
    cur.close()
    return "success"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
