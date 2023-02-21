import os, uuid, json
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

mysql = MySQL(server)


@server.route("/jobs", methods=["GET"])
def index():
    cur = mysql.connection.cursor()
    _ = cur.execute(f"SELECT * FROM Jobs")
    user_details = cur.fetchall()
    cur.close()
    return json.dumps(user_details)


@server.route("/add-job", methods=["POST"])
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
