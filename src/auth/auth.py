from dataclasses import dataclass
from functools import wraps
import requests, json, jwt, datetime, os
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

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@dataclass
class UserData:
    username: str
    user_type: str


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get(
            "Bearer"
        )  # http://localhost:5002/route?token=eydsafdsaf
        app.logger.info(token)
        if not token:
            return json.dumps({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except Exception as inst:
            app.logger.info(inst)
            return json.dumps({"message": "Token is missing or invalid"}), 401
        user_data = UserData(data["username"], data["user_type"])
        return f(user_data, *args, **kwargs)

    return decorated


@app.route("/auth/unprotected")
def unprotected():
    return "unprotected"


@app.route("/auth/protected")
@token_required
def protected(user_data):
    return f"user_data is: {user_data}"


@app.route("/auth/login", methods=["POST"])
def login():
    username, password = request.json["username"], request.json["password"]
    req = requests.get(
        "http://users:5000/users/check-info",
        json={"username": username, "password": password},
    )
    try:
        req.json()["message"]
        return req.json(), 401
    except:
        pass

    token = jwt.encode(
        {
            "username": username,
            "user_type": req.json()["user_type"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        app.config["SECRET_KEY"],
    )
    return json.dumps({"Bearer": token}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
