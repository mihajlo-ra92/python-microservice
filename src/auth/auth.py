import requests, json, jwt, datetime
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

app.config["SECRET_KEY"] = "verysecret"


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
    try:
        req.json()["text"]
        return req.json(), 401
    except:
        pass

    token = jwt.encode(
        {
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        app.config["SECRET_KEY"],
    )
    return json.dumps({"token": token}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
