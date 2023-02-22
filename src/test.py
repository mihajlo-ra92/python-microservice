import os, uuid, json
from flask import Flask, request

server = Flask(__name__)


@server.route("/bad-request", methods=["GET"])
def read_all():
    return "Some text", 400


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
