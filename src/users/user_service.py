from user_repo import UserRepo
from flask_mysqldb import MySQL


class UserService(object):
    def __init__(self, mysql: MySQL):
        self.repo = UserRepo(mysql)

    def read_all(self):
        return self.repo.read_all()

    def read_user(self, user_id):
        return self.repo.read_user(user_id)
