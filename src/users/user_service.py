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

    def create(self, user: User) -> User:
        return self.repo.create_user(user)

    def update(self, user: User) -> User:
        return self.repo.update_user(user)

    def delete_by_id(self, user_id) -> bool:
        return self.repo.delte_by_id(user_id)
