import requests, json
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/unprotected")
def unprotected():
    return "unprotected"


@app.route("/protected")
def protected():
    return "protected"


@app.route("/login", methods=["POST"])
def login():
    username, password = request.json["username"], request.json["password"]
    req = requests.get("http://users:5000/check-info")

    return f"uname: {username}, pass: {password}", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
