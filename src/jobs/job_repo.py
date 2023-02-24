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
        pass

    def update(self, job: Job) -> Job:
        pass

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
