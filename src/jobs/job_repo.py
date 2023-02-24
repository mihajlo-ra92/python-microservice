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
        # TODO: refactior into zip_data(cur)
        row_headers = [x[0] for x in cur.description]
        retVal = cur.fetchall()
        cur.close()
        json_data = []
        for result in retVal:
            json_data.append(dict(zip(row_headers, result)))
        jobs: list[Job] = json_data
        return jobs

    def read_by_id(self, job_id) -> Optional[Job]:
        pass

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
