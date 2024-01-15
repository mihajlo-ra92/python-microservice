from logging import Logger
import requests
from typing import Optional, Union
from application_repo import ApplicationRepo
from flask_mysqldb import MySQL
from application_model import MyException, Application, UserData
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

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("application_tracer")


class ApplicationService(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.logger = logger
        self.repo = ApplicationRepo(mysql, logger)

    def read_by_id(self, application_id: str) -> Optional[Application]:
        return self.repo.read_by_id(application_id)

    def read_by_worker_id(self, worker_id: str) -> list[Application]:
        applications: list[Application] = self.repo.read_by_worker_id(worker_id)
        for application in applications:
            try:
                reqWorker = requests.get(
                    "http://users:5000/users/read-by-id-safe",
                    json={"id": application.worker_id},
                )
                self.logger.info(f"recived reqWorker json: {reqWorker.json()}")
                application.worker = reqWorker.json()

                reqJob = requests.get(
                    "http://jobs:5000/jobs/read-by-id/" + application.job_id,
                )
                self.logger.info(f"recived reqJob json: {reqJob.json()}")
                application.job = reqJob.json()

            except Exception as ex:
                self.logger.error("Error retriving data from application service")
                self.logger.error(ex)
                return MyException("Error retriving data from application service")
        return applications

    def read_by_job_id(self, job_id: str) -> list[Application]:
        return self.repo.read_by_job_id(job_id)

    def create(self, application: Application) -> Union[Exception, Application]:
        return self.repo.create(application)

    def delete_by_id(self, application_id) -> bool:
        if self.repo.read_by_id_safe(application_id) == None:
            return False
        return self.repo.delete_by_id(application_id)
