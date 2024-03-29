import json, os
from typing import Optional, Union
from flask import request
from flask_cors import CORS
from application_model import Application, UserData
from application_utils import (
    read_application,
    read_decision,
    serialize_job,
    set_logger_config,
    set_start,
    token_required,
)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

from opentelemetry import trace, metrics
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace import Status, StatusCode
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from prometheus_client import start_http_server
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider

resource = Resource(attributes={"service.name": "application"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer("application_service")

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

start_http_server(port=8000, addr="0.0.0.0")
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = provider.get_meter("application-meter")
application_create_counter = meter.create_counter(
    name="application-create-counter", description="number of application creations"
)
application_decide_counter = meter.create_counter(
    name="application-decide-counter", description="number of application decisions"
)

set_logger_config()
[app, mysql, logger, service] = set_start()

CORS(app, origins="*", supports_credentials="*")


@app.route("/applications/read-by-id/<uuid:application_id>", methods=["GET"])
def read_by_id(application_id: str):
    application: Application = service.read_by_id(application_id)
    if application == None:
        return json.dumps({"message": "Invalid application_id"}), 400
    return json.dumps(application), 200


@app.route("/applications/read-by-worker-id/<uuid:worker_id>", methods=["GET"])
def read_by_worker_id(worker_id: str):
    applications: list[Application] = service.read_by_worker_id(worker_id)
    if applications == None:
        return json.dumps({"message": "No application found for sent worker_id"}), 404
    return json.dumps(applications, default=serialize_job), 200


@app.route("/applications/read-by-employer-id/<uuid:employer_id>", methods=["GET"])
def read_by_employer_id(employer_id: str):
    applications: list[Application] = service.read_by_employer_id(employer_id)
    if applications == None:
        return json.dumps({"message": "No application found for sent employer_id"}), 404
    return json.dumps(applications, default=serialize_job), 200


@app.route("/applications/read-by-job-id/<uuid:job_id>", methods=["GET"])
def read_by_job_id(job_id: str):
    application: Application = service.read_by_job_id(job_id)
    if application == None:
        return json.dumps({"message": "No application found for sent job_id"}), 404
    return json.dumps(application), 200


@app.route("/applications/decide/<uuid:application_id>", methods=["POST"])
def decide(application_id: str):
    with tracer.start_as_current_span("[POST] /applications/decide") as span:
        application_decide_counter.add(1)
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}
        application: Application = service.read_by_id(application_id)
        if application == None:
            return json.dumps({"message": "Invalid application_id"}), 400
        try:
            sent_decision: Application = read_decision(request.get_json())
            updated_application = service.decide(application_id, sent_decision,header)
        except Exception as ex:
            logger.info(ex)
            return json.dumps({"message": "Please send all application data"}), 400
        return json.dumps(updated_application, default=serialize_job), 200


@app.route("/applications/create", methods=["POST"])
def create():
    with tracer.start_as_current_span("[POST] /applications/create") as span:
        application_create_counter.add(1)
        try:
            sent_application: Application = read_application(request.json)
            logger.info("sent_application")
            logger.info(sent_application)
        except Exception as ex:
            logger.info(ex)
            return json.dumps({"message": "Please send all application data"}), 400
        retVal: Union[Exception, Application] = service.create(sent_application)
        logger.info("created")
        logger.info(retVal)
        if isinstance(retVal, Exception):
            return json.dumps({"message": str(retVal)}), 400
        return json.dumps(retVal, default=serialize_job), 201


def get_header_from_flask_request(request, key):
    return request.headers.get_all(key)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
