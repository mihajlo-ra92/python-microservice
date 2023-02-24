from logging import Logger
from typing import Optional, Union
from flask_mysqldb import MySQL
from job_repo import JobRepo
from job_model import MyException, Job, UserData


class JobService(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.logger = logger
        self.repo = JobRepo(mysql, logger)

    def read_all(self) -> list[Job]:
        return self.repo.read_all()

    def read_by_id(self, job_id: str) -> Optional[Job]:
        read_job = self.repo.read_by_id(job_id)
        return read_job

    def read_by_employer_id(self, employer_id: str) -> list[Job]:
        return self.repo.read_by_employer_id(employer_id)

    def read_by_worker_id(self, worker_id: str) -> list[Job]:
        return self.repo.read_by_worker_id(worker_id)

    def create(self, job: Job) -> Union[Exception, Job]:
        # TODO: Check if employer_id is valid
        # send http to users service to check
        return self.repo.create(job)

    def update(self, job: Job) -> Union[Exception, Job]:
        return self.repo.update(job)

    def delete_by_id(self, job_id: str) -> bool:
        return self.repo.delete_by_id(job_id)
