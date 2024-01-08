import json, os
from typing import Optional, Union
from flask import request
from flask_cors import CORS
from application_model import Application, UserData
from application_utils import (
    read_application,
    set_logger_config,
    set_start,
    token_required,
)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace import Status, StatusCode
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

resource = Resource(attributes={"service.name": "application_service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer("application_service")

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)


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
    application: Application = service.read_by_worker_id(worker_id)
    if application == None:
        return json.dumps({"message": "No application found for sent worker_id"}), 404
    return json.dumps(application), 200


@app.route("/applications/read-by-job-id/<uuid:job_id>", methods=["GET"])
def read_by_job_id(job_id: str):
    application: Application = service.read_by_job_id(job_id)
    if application == None:
        return json.dumps({"message": "No application found for sent job_id"}), 404
    return json.dumps(application), 200


@app.route("/applications/create", methods=["POST"])
def create():
    logger.info("start")
    logger.info(request)
    logger.info("json")
    logger.info(request.json)
    logger.info("worker_id")
    logger.info(request.json["worker_id"])
    logger.info("job_id")
    logger.info(request.json["job_id"])
    logger.info("description")
    logger.info(request.json["description"])
    try:
        sent_application: Application = read_application(request.json)
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": "Please send all application data"}), 400
    retVal: Union[Exception, Application] = service.create(sent_application)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return retVal.toJSON(), 201


def get_header_from_flask_request(request, key):
    return request.headers.get_all(key)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
