import json
from flask import request
from job_model import Job
from flask_cors import CORS
from typing import Optional, Union

from job_utils import read_job, set_logger_config, set_start, serialize_job

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
    retVal: Union[Exception, list[Job]] = service.read_open()
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/read-by-id/<uuid:job_id>", methods=["GET"])
def read_by_id(job_id):
    retVal: Optional[Job] = service.read_by_id(job_id)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)})
    return json.dumps(retVal, default=serialize_job), 200

@app.route("/jobs/read-by-employer-id/<uuid:employer_id>", methods=["GET"])
def read_by_employer_id(employer_id):
    retVal: Union[Exception, list[Job]] = service.read_by_employer_id(employer_id)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return json.dumps(retVal, default=serialize_job), 200


@app.route("/jobs/create", methods=["POST"])
def create_job():
    try:
        sent_job: Job = read_job(request.json)
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": "Please send all job data"}), 400
    retVal: Union[Exception, Job] = service.create(sent_job)
    if isinstance(retVal, Exception):
        return json.dumps({"message": str(retVal)}), 400
    return retVal.toJSON(), 201


@app.route("/jobs/update", methods=["PUT"])
def update_job():
    try:
        sent_job: Job = read_job(request.json)
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
