from logging import Logger
from typing import Optional, Union
from user_repo import UserRepo
from flask_mysqldb import MySQL
from user_model import MyException, User, UserData
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
tracer = trace.get_tracer("user_tracer")


class UserService(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.logger = logger
        self.repo = UserRepo(mysql, logger)

    def read_all(self) -> list[User]:
        with tracer.start_as_current_span("service.read_all") as child:
            return self.repo.read_all()

    def read_by_id_unsafe(self, user_id: str) -> Optional[User]:
        read_user = self.repo.read_by_id_unsafe(user_id)
        if read_user != None:
            read_user["password"] = None
        return read_user

    def read_by_id_safe(self, user_id: str) -> Optional[User]:
        read_user = self.repo.read_by_id_safe(user_id)
        if read_user != None:
            read_user["password"] = None
        return read_user

    def read_by_username(self, username: str) -> Optional[User]:
        read_user = self.repo.read_by_username(username)
        if read_user != None:
            read_user["password"] = None
        return read_user

    def read_logged_user(self, username: str) -> Optional[User]:
        read_user = self.repo.read_by_username(username)
        return read_user

    def create(self, user: User) -> Union[Exception, User]:
        return self.repo.create(user)

    def update(self, user: User, logged_user: UserData) -> Union[Exception, User]:
        user_to_be_changed: User = self.repo.read_by_id_safe(user.id)
        if user_to_be_changed == None:
            return MyException("No user with such id")
        if (
            user_to_be_changed["username"] == logged_user.username
            or logged_user.user_type == "ADMIN"
        ):
            return self.repo.update(user)
        return MyException("Only admin can update other users")

    def delete_by_id(self, user_id) -> bool:
        if self.repo.read_by_id_safe(user_id) == None:
            return False
        return self.repo.delete_by_id(user_id)

    def check_info(self, username, password) -> Union[str, tuple[str, str]]:
        with tracer.start_as_current_span("service.check_info") as child:
            read_user = self.repo.read_by_username(username)
            if read_user == None:
                return "Username invalid"
            if read_user["password"] != password:
                return "Password invalid"
            return [read_user["username"], read_user["user_type"]]
