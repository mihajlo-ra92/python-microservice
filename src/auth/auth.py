import requests, json
from flask import Flask, jsonify, request
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
    req = requests.get(
        "http://users:5000/check-info",
        json={"username": username, "password": password},
    )

    return req.json(), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
