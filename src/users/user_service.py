from user_repo import UserRepo
from flask_mysqldb import MySQL
from user_model import User


class UserService(object):
    def __init__(self, mysql: MySQL):
        self.repo = UserRepo(mysql)

    def read_all(self) -> list[User]:
        return self.repo.read_all()

    def read_user(self, user_id) -> User:
        return self.repo.read_user(user_id)

    def create_user(self, user: User) -> User:
        return self.repo.create_user(user)

    def update_user(self, user: User) -> User:
        return self.repo.update_user(user)
