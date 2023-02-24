import json, uuid
from typing import Optional, Union
from logging import Logger
from flask_mysqldb import MySQL

from job_model import Job


class JobRepo(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.mysql = mysql
        self.logger = logger

    def read_all(self) -> list[Job]:
        cur = self.mysql.connection.cursor()
        cur.execute(
            f"SELECT id, employer_id, worker_id,\
        job_name, job_desc, pay_in_euro,\
        completed FROM Jobs"
        )
        return zip_data(cur)

    def read_by_id(self, job_id) -> Optional[Job]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Jobs WHERE id='{job_id}';")
        jobs = zip_data(cur)
        if len(jobs) > 0:
            return jobs[0]
        return None

    def read_by_employer_id(self, employer_id) -> list[Job]:
        pass

    def read_by_worker_id(self, worker_id) -> list[Job]:
        pass

    def create(self, job: Job) -> Union[Exception, Job]:
        job.id = str(uuid.uuid1())
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                f"INSERT INTO Jobs(id, employer_id, worker_id, job_name, \
        job_desc, pay_in_euro, completed) VALUES('{str(uuid.uuid1())}', \
        '{job.employer_id}', NULL, '{job.job_name}', '{job.job_desc}', \
        '{job.pay_in_euro}', false);"
            )
        except Exception as ex:
            self.logger.info(ex)
            return ex
        self.mysql.connection.commit()
        cur.close()
        job.worker_id = None
        job.completed = False
        return job

    def update(self, job: Job) -> Job:
        cur = self.mysql.connection.cursor()
        cur.execute(
            f"UPDATE Jobs\
            SET employer_id='{job.employer_id}',worker_id='{job.worker_id}',\
            job_name='{job.job_name}',job_desc='{job.job_desc}',\
            pay_in_euro={job.pay_in_euro},completed={job.completed}\
            WHERE id='{job.id}';"
        )
        self.mysql.connection.commit()
        cur.close()
        return job

    def delete_by_id(self, job_id: str) -> bool:
        pass


def zip_data(cur) -> list[Job]:
    row_headers = [x[0] for x in cur.description]
    retVal = cur.fetchall()
    cur.close()
    json_data = []
    for result in retVal:
        json_data.append(dict(zip(row_headers, result)))
    jobs: list[Job] = json_data
    return jobs
