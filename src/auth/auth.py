from dataclasses import dataclass
import requests, json, jwt, datetime, os
from flask import Flask, request
from flask_cors import CORS
from logging.config import dictConfig
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace, metrics
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server


resource = Resource(attributes={"service.name": "auth"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer("user_service")
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# resource = Resource(attributes={
#     SERVICE_NAME: "auth-service"
# })
# Start Prometheus client
start_http_server(port=8000, addr="0.0.0.0")
# Initialize PrometheusMetricReader which pulls metrics from the SDK
# on-demand to respond to scrape requests
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = provider.get_meter("auth-meter")
login_counter = meter.create_counter(
    name="login-counter", description="number of successful logins"
)


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
CORS(app, origins="*", supports_credentials="*")

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
            login_counter.add(1)
            req.json()["message"]
            return req.json(), 401
        except:
            pass

        token = jwt.encode(
            {
                "user_id": req.json()["user_id"],
                "username": username,
                "user_type": req.json()["user_type"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            app.config["SECRET_KEY"],
        )
        span.set_status(Status(StatusCode.OK))
        return (
            json.dumps(
                {
                    "Bearer": token,
                    "user_type": req.json()["user_type"],
                    "user_id": req.json()["user_id"],
                }
            ),
            201,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
