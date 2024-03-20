from logging import Logger
from typing import Optional, Union
from flask_mysqldb import MySQL
from job_repo import JobRepo
from job_model import MyException, Job, UserData
import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry import trace

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("job_tracer")


class JobService(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.logger = logger
        self.repo = JobRepo(mysql, logger)

    def read_all(self) -> Union[Exception, list[Job]]:
        jobs: list[Job] = self.repo.read_all()
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

    def read_open(self, header) -> Union[Exception, list[Job]]:
        with tracer.start_as_current_span("service.read_open") as child:
            jobs: list[Job] = self.repo.read_open()
            for job in jobs:
                try:
                    reqEmployer = requests.get(
                        "http://users:5000/users/read-by-id-safe",
                        json={"id": job.employer_id},
                        headers=header,
                    )
                    self.logger.info(f"recived reqEmployer json: {reqEmployer.json()}")
                    job.employer = reqEmployer.json()

                    if job.worker_id != None and job.worker_id != "":
                        reqWorker = requests.get(
                            "http://users:5000/users/read-by-id-safe",
                            json={"id": job.worker_id},
                            headers=header,
                        )
                        self.logger.info(f"recived reqWorker json: {reqWorker.json()}")
                        job.worker = reqWorker.json()

                except Exception as ex:
                    self.logger.error("Error retriving data from user service")
                    self.logger.error(ex)
                    return MyException("Error retriving data from user service")
            return jobs

    def read_by_id(self, job_id: str, headers) -> Union[Exception, Job]:
        job: Optional[Job] = self.repo.read_by_id(job_id)
        if job is None:
            return MyException("Falied to retrive job")
        try:
            reqEmployer = requests.get(
                "http://users:5000/users/read-by-id-safe",
                json={"id": job.employer_id},
                headers=headers,
            )
            self.logger.info(f"recived reqEmployer json: {reqEmployer.json()}")
            job.employer = reqEmployer.json()

            if job.worker_id != None and job.worker_id != "":
                reqWorker = requests.get(
                    "http://users:5000/users/read-by-id-safe",
                    json={"id": job.worker_id},
                    headers=headers,
                )
                self.logger.info(f"recived reqWorker json: {reqWorker.json()}")
                job.worker = reqWorker.json()

        except Exception as ex:
            self.logger.error("Error retriving data from user service")
            self.logger.error(ex)
            return MyException("Error retriving data from user service")
        return job

    def read_by_employer_id(self, employer_id: str) -> Union[Exception, list[Job]]:
        jobs: list[Job] = self.repo.read_by_employer_id(employer_id)
        # TODO: create separate function
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

    def read_by_worker_id(self, worker_id: str) -> list[Job]:
        return self.repo.read_by_worker_id(worker_id)

    def finished_read_by_worker_id(self, worker_id: str) -> Union[Exception, list[Job]]:
        jobs: list[Job] = self.repo.finished_read_by_worker_id(worker_id)
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

    def create(self, job: Job, header) -> Union[Exception, Job]:
        with tracer.start_as_current_span("service.create") as child:
            req = requests.get(
                "http://users:5000/users/read-by-id-safe",
                json={"id": job.employer_id},
                headers=header,
            )
            self.logger.info(f"recived req json: {req.json()}")
            try:
                if req.json()["message"] == "Invalid user_id":
                    return MyException("Sent employer_id not valid")
            except Exception as ex:
                if req.json()["user_type"] != "EMPLOYER":
                    return MyException("Sent employer_id must be of an employer")
            return self.repo.create(job)

    def complete(self, job_id: str) -> Union[Exception, Job]:
        with tracer.start_as_current_span("service.complete") as child:
            self.repo.complete(job_id)
            return self.repo.read_by_id(job_id)

    def assign_worker(self, job_id: str, worker_id: str) -> Union[Exception, Job]:
        with tracer.start_as_current_span("service.assign_worker") as child:
            self.logger.info("service")
            self.repo.assign_worker(job_id, worker_id)
            self.logger.info("assigned")
            return self.repo.read_by_id(job_id)

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
