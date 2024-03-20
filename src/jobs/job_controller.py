import json
from flask import request
from job_model import Job
from flask_cors import CORS
from typing import Optional, Union

from job_utils import (
    read_job,
    read_job_update,
    set_logger_config,
    set_start,
    serialize_job,
)

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

resource = Resource(attributes={"service.name": "jobs"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer("jobs_service")
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

start_http_server(port=8000, addr="0.0.0.0")
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = provider.get_meter("jobs-meter")
job_read_open_counter = meter.create_counter(
    name="job-read-open-counter", description="number of open job retrivals"
)
job_create_counter = meter.create_counter(
    name="job-create-counter", description="number of open jobs created"
)

set_logger_config()
[app, mysql, logger, service] = set_start()

CORS(app, origins="*", supports_credentials="*")


@app.route("/jobs/read-all", methods=["GET"])
def read_jobs():
    retVal: Union[Exception, list[Job]] = service.read_all()
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/read-open", methods=["GET"])
def read_open():
    with tracer.start_as_current_span("[GET] /jobs/read-open") as span:
        logger.info("before add1")
        job_read_open_counter.add(1)
        logger.info("after add1")
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}
        retVal: Union[Exception, list[Job]] = service.read_open(header)
        if isinstance(retVal, Exception):
            return json.dumps({"message": str(retVal)}), 400
        span.set_status(Status(StatusCode.OK))
        return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/read-by-id/<uuid:job_id>", methods=["GET"])
def read_by_id(job_id):
    with tracer.start_as_current_span("[GET] /jobs/read-by-id") as span:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}
        retVal: Optional[Job] = service.read_by_id(job_id, header)
        if isinstance(retVal, Exception):
            return json.dumps({"message": str(retVal)})
        return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/read-by-employer-id/<uuid:employer_id>", methods=["GET"])
def read_by_employer_id(employer_id):
    retVal: Union[Exception, list[Job]] = service.read_by_employer_id(employer_id)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/finished/read-by-worker-id/<uuid:worker_id>", methods=["GET"])
def finished_read_by_worker_id(worker_id):
    retVal: Union[Exception, list[Job]] = service.finished_read_by_worker_id(worker_id)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/assign-worker", methods=["POST"])
def assign_user():
    traceparent = request.headers.get("traceparent")
    if traceparent is None:
        span = tracer.start_span("[POST] /jobs/assign-worker")
    else:
        carrier = {"traceparent": traceparent}
        ctx = TraceContextTextMapPropagator().extract(carrier)
        span = tracer.start_span("[POST] /jobs/assign-worker", context=ctx)

    with span:
        worker_id = request.json["worker_id"]
        job_id = request.json["job_id"]
        retVal: Optional[Job] = service.assign_worker(job_id, worker_id)
        if isinstance(retVal, Exception):
            return json.dumps({"message": str(retVal)})
        return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/complete/<uuid:job_id>", methods=["POST"])
def complete(job_id):
    retVal: Optional[Job] = service.complete(job_id)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)})
    return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/create", methods=["POST"])
def create_job():
    with tracer.start_as_current_span("[POST] /jobs/create") as span:
        job_create_counter.add(1)
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}
        try:
            sent_job: Job = read_job(request.json)
        except Exception as ex:
            logger.info(ex)
            return json.dumps({"message": "Please send all job data"}), 400
        retVal: Union[Exception, Job] = service.create(sent_job, header)
        if isinstance(retVal, Exception):
            return json.dumps({"message": str(retVal)}), 400
        return retVal.toJSON(), 201


@app.route("/jobs/update", methods=["PUT"])
def update_job():
    try:
        sent_job: Job = read_job_update(request.json)
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": "Please send all user data"}), 400
    retVal: Union[Exception, Job] = service.update(sent_job)
    if isinstance(retVal, Job):
        return retVal.toJSON(), 201
    return json.dumps({"message": str(retVal)}), 401


@app.route("/jobs/delete", methods=["DELETE"])
def delete_job():
    try:
        job_id = request.json["id"]
    except Exception as ex:
        return json.dumps({"message": "Please send id"}), 400
    deleted: bool = service.delete_by_id(job_id)
    return json.dumps(deleted), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
