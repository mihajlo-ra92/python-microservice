from logging import Logger
from typing import Optional, Union
from user_repo import UserRepo
from flask_mysqldb import MySQL
from user_model import User


class UserService(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.logger = logger
        self.repo = UserRepo(mysql, logger)

    def read_all(self) -> list[User]:
        self.logger.info("!!! FROM SERVICE !!!")
        return self.repo.read_all()

    def read_by_id(self, user_id: str) -> Optional[User]:
        read_user = self.repo.read_by_id(user_id)
        if read_user != None:
            read_user["password"] = None
        return read_user

    def read_by_username(self, username: str) -> Optional[User]:
        read_user = self.repo.read_by_username(username)
        if read_user != None:
            read_user["password"] = None
        return read_user

    def create(self, user: User) -> User:
        return self.repo.create(user)

    def update(self, user: User) -> User:
        return self.repo.update(user)

    def delete_by_id(self, user_id) -> bool:
        return self.repo.delete_by_id(user_id)

    def check_info(self, username, password) -> Union[str, tuple[str, str]]:
        read_user = self.repo.read_by_username(username)
        if read_user == None:
            return "Username invalid"
        if read_user["password"] != password:
            return "Password invalid"
        return [read_user["username"], read_user["user_type"]]
