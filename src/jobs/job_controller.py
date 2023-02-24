import os, uuid, json
from flask import request
from job_model import Job
from typing import Optional, Union

from job_utils import read_job, set_logger_config, set_start

set_logger_config()
[app, mysql, logger, service] = set_start()


@app.route("/init-test")
def init_test_db():
    if os.environ.get("TEST") == "TRUE":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Jobs;")
        cur.execute(
            "INSERT INTO Jobs (id, employer_id, worker_id,\
        job_name, job_desc, pay_in_euro, completed)\
        VALUES ('job1','employer1', 'worker1', 'name1', 'desc1', 1.0, true),\
        ('job2','employer1', 'worker2', 'name2', 'desc2', 2.0, false),\
        ('job3','employer2', 'worker1', 'name3', 'desc3', 3.0, true),\
        ('job4','employer2', 'worker2', 'name4', 'desc4', 4.0, true),\
        ('job5','employer1', NULL, 'name5', 'desc5', 5.0, false);"
        )
        mysql.connection.commit()
        users_db_test = os.environ.get("MYSQL_DB_USERS") + "_test"
        logger.info(f"usersDB: {users_db_test}")
        cur.execute(f"USE {users_db_test}")
        cur.execute("DELETE FROM Users;")
        cur.execute(
            "INSERT INTO Users (id, username, password, email, \
        user_type) VALUES ('employer1',\
        'emp_us_1', '123', 'test1@gmail.com', 'EMPLOYER'),\
        ('worker1',\
        'test2', '123', 'test2@gmail.com', 'WORKER'), \
        ('33333333-b392-11ed-92c6-0242ac170004',\
        'test3', '123', 'test3@gmail.com', 'ADMIN');"
        )
        jobs_db_test = os.environ.get("MYSQL_DB_JOBS") + "_test"
        logger.info(f"jobsDB: {jobs_db_test}")
        cur.execute(f"USE {jobs_db_test}")
        mysql.connection.commit()
        cur.close()
    return ""


@app.route("/read-jobs", methods=["GET"])
def read_jobs():
    jobs: list[Job] = service.read_all()
    return json.dumps(jobs), 200


@app.route("/read-by-id", methods=["GET"])
def read_by_id():
    sent_job = request.json
    try:
        job_id = sent_job["id"]
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": "Please send id"}), 400
    job: Optional[Job] = service.read_by_id(job_id)
    if job == None:
        return json.dumps({"message": "Invalid job_id"})
    return json.dumps(job), 200


@app.route("/create-job", methods=["POST"])
def create_job():
    try:
        sent_job: Job = read_job(request.json)
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": "Please send all job data"}), 400
    retVal: Union[Exception, Job] = service.create(sent_job)
    if isinstance(retVal, Job):
        return retVal.toJSON(), 201
    return json.dumps({"message": str(retVal)}), 400


@app.route("/update-job", methods=["PUT"])
def update_job():
    job = request.json
    job_id = job["id"]
    worker_id = job["workerId"]
    job_name = job["jobName"]
    job_desc = job["jobDesc"]
    pay_in_euro = job["payInEuro"]
    completed = job["completed"]
    cur = mysql.connection.cursor()
    if worker_id == None and completed == 0:
        cur.execute(
            f"UPDATE Jobs \
                    SET job_name = '{job_name}', job_desc = '{job_desc}', \
                    pay_in_euro = {pay_in_euro}, completed = {completed}, \
                    worker_id = '{worker_id}'\
                    WHERE id = '{job_id}';"
        )
        mysql.connection.commit()
        cur.close()
        return json.dumps(job)
    message = "Cannot update job where a worker is assigned or a job that \
    is completed"
    return json.dumps(message)


@app.route("/delete-job", methods=["DELETE"])
def delete_job():
    job = request.json
    job_id = job["id"]
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Jobs WHERE id='{job_id}';")
    mysql.connection.commit()
    cur.close()
    return json.dumps(job)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
