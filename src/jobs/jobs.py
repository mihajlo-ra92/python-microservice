import os, uuid, json
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

mysql = MySQL(server)


@server.route("/read-jobs", methods=["GET"])
def read_jobs():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Jobs")
    jobs = cur.fetchall()
    cur.close()
    return json.dumps(jobs)


@server.route("/read-job", methods=["GET"])
def read_job():
    sent_job = request.json
    job_id = sent_job["id"]
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Jobs WHERE id='{job_id}';")
    read_job = cur.fetchall()
    cur.close()
    return json.dumps(read_job)


@server.route("/create-job", methods=["POST"])
def create_job():
    job = request.json
    empoloyer_id = job["employerId"]
    job_name = job["jobName"]
    job_desc = job["jobDesc"]
    pay_in_euro = job["payInEuro"]
    completed = job["completed"]

    cur = mysql.connection.cursor()
    cur.execute(
        f"INSERT INTO Jobs(id, employer_id, worker_id, job_name, \
        job_desc, pay_in_euro, completed) VALUES('{str(uuid.uuid1())}', \
        '{empoloyer_id}', NULL, '{job_name}', '{job_desc}', \
        '{pay_in_euro}', {completed});"
    )
    mysql.connection.commit()
    cur.close()
    return json.dumps(job)


@server.route("/update-job", methods=["PUT"])
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


@server.route("/delete-job", methods=["DELETE"])
def delete_job():
    job = request.json
    job_id = job["id"]
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Jobs WHERE id='{job_id}';")
    mysql.connection.commit()
    cur.close()
    return json.dumps(job)


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
