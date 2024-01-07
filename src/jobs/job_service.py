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

    def read_all(self) -> Union[Exception, list[Job]]:
        jobs:list[Job] = self.repo.read_all()
        for job in jobs:
            try:
                reqEmployer = requests.get(
                    "http://users:5000/users/read-by-id-safe",
                    json={"id": job.employer_id},
                )
                self.logger.info(f"recived reqEmployer json: {reqEmployer.json()}")
                job.employer = reqEmployer.json()

                if job.worker_id != None and job.worker_id != "":
                    reqWorker = requests.get(
                        "http://users:5000/users/read-by-id-safe",
                        json={"id": job.worker_id},
                    )
                    self.logger.info(f"recived reqWorker json: {reqWorker.json()}")
                    job.worker = reqWorker.json()

            except Exception as ex:
                self.logger.error("Error retriving data from user service")
                self.logger.error(ex)
                return MyException("Error retriving data from user service")
        return jobs

    def read_open(self) -> Union[Exception, list[Job]]:
        jobs:list[Job] = self.repo.read_open()
        for job in jobs:
            try:
                reqEmployer = requests.get(
                    "http://users:5000/users/read-by-id-safe",
                    json={"id": job.employer_id},
                )
                self.logger.info(f"recived reqEmployer json: {reqEmployer.json()}")
                job.employer = reqEmployer.json()

                if job.worker_id != None and job.worker_id != "":
                    reqWorker = requests.get(
                        "http://users:5000/users/read-by-id-safe",
                        json={"id": job.worker_id},
                    )
                    self.logger.info(f"recived reqWorker json: {reqWorker.json()}")
                    job.worker = reqWorker.json()

            except Exception as ex:
                self.logger.error("Error retriving data from user service")
                self.logger.error(ex)
                return MyException("Error retriving data from user service")
        return jobs


    def read_by_id(self, job_id: str) -> Union[Exception,Job]:
        job: Optional[Job] = self.repo.read_by_id(job_id)
        if job is None:
            return MyException("Falied to retrive job")
        try:
            reqEmployer = requests.get(
                "http://users:5000/users/read-by-id-safe",
                json={"id": job.employer_id},
            )
            self.logger.info(f"recived reqEmployer json: {reqEmployer.json()}")
            job.employer = reqEmployer.json()

            if job.worker_id != None and job.worker_id != "":
                reqWorker = requests.get(
                    "http://users:5000/users/read-by-id-safe",
                    json={"id": job.worker_id},
                )
                self.logger.info(f"recived reqWorker json: {reqWorker.json()}")
                job.worker = reqWorker.json()

        except Exception as ex:
            self.logger.error("Error retriving data from user service")
            self.logger.error(ex)
            return MyException("Error retriving data from user service")
        return job

    def read_by_employer_id(self, employer_id: str) -> list[Job]:
        return self.repo.read_by_employer_id(employer_id)

    def read_by_worker_id(self, worker_id: str) -> list[Job]:
        return self.repo.read_by_worker_id(worker_id)

    def create(self, job: Job) -> Union[Exception, Job]:
        req = requests.get(
            "http://users:5000/users/read-by-id-safe", json={"id": job.employer_id}
        )
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
