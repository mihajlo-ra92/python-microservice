import json, os
from typing import Optional, Union
from flask import request
from flask_cors import CORS
from user_model import User, UserData
from user_utils import read_user, set_logger_config, set_start, token_required
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace import Status, StatusCode
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

resource = Resource(attributes={"service.name": "user_service"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer("user_service")

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)


set_logger_config()
[app, mysql, logger, service] = set_start()

CORS(app, origins="*", supports_credentials="*")


@app.route("/users/init-test")
def init_test_db():
    if os.environ.get("TEST") == "TRUE":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Users;")
        cur.execute(
            "INSERT INTO Users (id, username, password, email, \
        user_type) VALUES ('43299a1e-b392-11ed-92c6-0242ac170004',\
        'test1', '123', 'test1@gmail.com', 'WORKER'),\
        ('22222222-b392-11ed-92c6-0242ac170004',\
        'test2', '123', 'test2@gmail.com', 'EMPLOYER'), \
        ('33333333-b392-11ed-92c6-0242ac170004',\
        'test3', '123', 'test3@gmail.com', 'ADMIN');"
        )
        mysql.connection.commit()

        cur.close()
    return ""


@app.route("/users/read-all", methods=["GET"])
def read_all():
    with tracer.start_as_current_span("[GET] /users/read-all") as span:
        users: list[User] = service.read_all()
        span.set_status(Status(StatusCode.OK))
        return json.dumps(users), 200


@app.route("/users/read-by-id-unsafe", methods=["GET"])
def read_by_id_unsafe():
    sent_user = request.json
    try:
        user_id = sent_user["id"]
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send id"}), 400
    user: Optional[User] = service.read_by_id_unsafe(user_id)
    if user == None:
        return json.dumps({"message": "Invalid user_id"}), 400
    return json.dumps(user), 200


@app.route("/users/read-by-id-safe", methods=["GET"])
def read_by_id_safe():
    traceparent = request.headers.get("traceparent")
    if traceparent is None:
        span = tracer.start_span("[GET] /users/read-by-id-safe")
    else:
        carrier = {"traceparent": traceparent}
        ctx = TraceContextTextMapPropagator().extract(carrier)
        span = tracer.start_span("[GET] /users/read-by-id-safe", context=ctx)

    with span:
        sent_user = request.json
        try:
            user_id = sent_user["id"]
        except Exception as inst:
            logger.info(inst)
            return json.dumps({"message": "Please send id"}), 400
        user: Optional[User] = service.read_by_id_safe(user_id)
        if user == None:
            return json.dumps({"message": "Invalid user_id"}), 400
        span.set_status(Status(StatusCode.OK))
        return json.dumps(user), 200


# NOTE: Reads by username in jwt
@app.route("/users/read-logged-in", methods=["GET"])
@token_required
def read_logged_user(user_data):
    logged_user: UserData = user_data
    username = logged_user.username
    user: User = service.read_logged_user(username)
    if user == None:
        return json.dumps({"message": "Invalid username"}), 400
    return json.dumps(user), 200


@app.route("/users/read-by-username/<string:username>", methods=["GET"])
def read_by_username(username):
    user: User = service.read_by_username(username)
    if user == None:
        return json.dumps({"message": "Invalid username"}), 400
    return json.dumps(user), 200


@app.route("/users/create", methods=["POST"])
def create():
    try:
        sent_user: User = read_user(request.json)
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send all user data"}), 400
    retVal: Union[Exception, User] = service.create(sent_user)
    if isinstance(retVal, User):
        return retVal.toJSON(), 201
    return json.dumps({"message": str(retVal)}), 400


@app.route("/users/update", methods=["PUT"])
@token_required
def update(logged_user: UserData):
    logger.info(f"Logged user: {logged_user}")
    try:
        sent_user: User = read_user(request.json)
    except Exception as inst:
        logger.info(inst)
        return json.dumps({"message": "Please send all user data"}), 400
    retVal: Union[Exception, User] = service.update(sent_user, logged_user)
    if isinstance(retVal, User):
        return retVal.toJSON(), 201
    return json.dumps({"message": str(retVal)}), 401


@app.route("/users/delete", methods=["DELETE"])
@token_required
def delete(user_data):
    # TODO: check jwt, user must be admin ar ids must match
    # TODO: check request.json for id, if invalid send bad request
    # sent_user: User = request.json
    deleted: bool = service.delete_by_id(request.json["id"])
    return json.dumps(deleted), 200


def get_header_from_flask_request(request, key):
    return request.headers.get_all(key)


@app.route("/users/check-info", methods=["GET"])
def check_info():
    traceparent = get_header_from_flask_request(request, "traceparent")
    carrier = {"traceparent": traceparent[0]}
    ctx = TraceContextTextMapPropagator().extract(carrier)
    with tracer.start_as_current_span("[GET] /users/check-info", context=ctx) as span:
        try:
            username, password = request.json["username"], request.json["password"]
        except Exception as inst:
            logger.info(inst)
            return json.dumps({"message": "Please send username and password"}), 400
        jwt_data: Union[str, tuple[str, str]] = service.check_info(username, password)
        logger.info(jwt_data)
        if jwt_data == "Username invalid":
            return json.dumps({"message": jwt_data}), 401
        if jwt_data == "Password invalid":
            return json.dumps({"message": jwt_data}), 401
        span.set_status(Status(StatusCode.OK))
        return json.dumps(
            {"username": jwt_data[0], "user_type": jwt_data[1], "user_id": jwt_data[2]}
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
