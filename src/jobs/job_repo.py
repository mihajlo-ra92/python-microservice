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
        pass

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
