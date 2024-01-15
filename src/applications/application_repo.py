import uuid
from typing import Optional, Union
from logging import Logger
from flask_mysqldb import MySQL
from application_model import Application
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


class ApplicationRepo(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.mysql = mysql
        self.logger = logger

    def read_by_id(self, application_id) -> Optional[Application]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Applications WHERE id='{application_id}';")
        applications = self.zip_data(cur)
        if len(applications) > 0:
            return applications[0]
        return None

    def read_by_worker_id(self, worker_id) -> list[Application]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Applications WHERE worker_id='{worker_id}';")
        return self.zip_data(cur)

    def read_by_job_id(self, job_id) -> list[Application]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Applications WHERE job_id='{job_id}';")
        return self.zip_data(cur)

    def create(self, application: Application) -> Union[Exception, Application]:
        application.id = str(uuid.uuid1())
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                f"INSERT INTO Applications(id, worker_id, job_id, description) VALUES \
                ('{application.id}', '{application.worker_id}', '{application.job_id}', '{application.description}');"
            )
        except Exception as ex:
            self.logger.info(ex)
            return ex
        self.mysql.connection.commit()
        cur.close()
        return application

    # TODO: Implement update

    def delete_by_id(self, application_id: str) -> bool:
        cur = self.mysql.connection.cursor()
        cur.execute(f"DELETE FROM Applications WHERE id='{application_id}';")
        self.mysql.connection.commit()
        cur.close()
        return True

    def zip_data(self, cur) -> list[Application]:
        row_headers = [x[0] for x in cur.description]
        result_set = cur.fetchall()
        cur.close()

        applications = []
        for result in result_set:
            self.logger.info("result iter")
            self.logger.info(result)
            application_data = dict(zip(row_headers, result))
            self.logger.info("item")
            self.logger.info(application_data)
            application = Application(**application_data)
            applications.append(application)

        return applications
