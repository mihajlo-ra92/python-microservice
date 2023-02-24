from logging import Logger
from typing import Optional, Union
from flask_mysqldb import MySQL
from job_repo import JobRepo
from job_model import MyException, Job, UserData
import requests


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
        req = requests.get("http://users:5000/read-by-id", json={"id": job.employer_id})
        self.logger.info(f"recived req json: {req.json()}")
        try:
            if req.json()["message"] == "Invalid user_id":
                return MyException("Sent employer_id not valid")
        except Exception as ex:
            if req.json()["user_type"] != "EMPLOYER":
                return MyException("Sent employer_id must be of an employer")

        return self.repo.create(job)

    def update(self, job: Job) -> Union[Exception, Job]:
        self.logger.info(f"sent job: {job.toJSON()}")
        job_to_be_changed: Job = self.repo.read_by_id(job.id)
        self.logger.info(f"job to change: {job_to_be_changed}")
        if job_to_be_changed == None:
            return MyException("No job with such id")
        return self.repo.update(job)

    def delete_by_id(self, job_id: str) -> bool:
        if self.repo.read_by_id(job_id) == None:
            return False
        return self.repo.delete_by_id(job_id)
