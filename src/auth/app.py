import jwt, datetime, os, uuid
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import mysql.connector

server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

mydb2 = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
)
mysql = MySQL(server)


@server.route("/", methods=["GET"])
def welcome():
    return [
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_HOST"),
        os.environ.get("MYSQL_PASSWORD"),
        os.environ.get("MYSQL_PORT"),
        os.environ.get("MYSQL_PASSWORD"),
        os.environ.get("MYSQL_DB"),
    ]


@server.route("/read-table", methods=["GET"])
def read_table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mytable")
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@server.route("/add-to-table", methods=["POST"])
def add_to_table():
    if request.is_json:
        item = request.get_json()
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO mytable (id, name, age) VALUES (%s, %s, %s)",
                (uuid.uuid1(), item["name"], item["age"]),
            )
            mysql.connection.commit()
            cur.close()
            response = {"status": "success", "message": "Item added successfully!"}
            return jsonify(response), 201
        except:
            response = {
                "status": "error",
                "message": "An error occurred while adding the item to the database.",
            }
            return jsonify(response), 500
    else:
        response = {"status": "error", "message": "Request must be in JSON format."}
        return jsonify(response), 400


@server.route("/create-table", methods=["GET"])
def create_table():
    cur = mysql.connection.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mytable (
            id VARCHAR(255) PRIMARY KEY ,
            name VARCHAR(255),
            age INT
        )
    """
    )
    cur.close()
    return "Table created successfully!"


@server.route("/create-table2", methods=["GET"])
def create_table():
    cur = mysql.connection.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mytable (
            id VARCHAR(255) PRIMARY KEY ,
            name VARCHAR(255),
            age INT
        )
    """
    )
    cur.close()
    return "Table created successfully!"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
