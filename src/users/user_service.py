from logging import Logger
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

    def read_by_id(self, user_id: str) -> User:
        return self.repo.read_by_id(user_id)

    def read_by_username(self, username: str) -> User:
        return self.repo.read_by_username(username)

    def create(self, user: User) -> User:
        return self.repo.create(user)

    def update(self, user: User) -> User:
        return self.repo.update(user)

    def delete_by_id(self, user_id) -> bool:
        return self.repo.delete_by_id(user_id)
