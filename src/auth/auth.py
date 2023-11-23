from dataclasses import dataclass
import requests, json, jwt, datetime, os
from flask import Flask, request
from logging.config import dictConfig
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

resource = Resource(attributes={"service.name": "auth"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer("user_service")

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

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


@app.route("/auth/login", methods=["POST"])
def login():
    with tracer.start_as_current_span("[POST] /auth/login") as span:
        username, password = request.json["username"], request.json["password"]
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}
        req = requests.get(
            "http://users:5000/users/check-info",
            json={"username": username, "password": password},
            headers=header,
        )
        try:
            req.json()["message"]
            return req.json(), 401
        except:
            pass

        token = jwt.encode(
            {
                # TODO: Maybe add userId
                "username": username,
                "user_type": req.json()["user_type"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            app.config["SECRET_KEY"],
        )
        span.set_status(Status(StatusCode.OK))
        return json.dumps({"Bearer": token}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
