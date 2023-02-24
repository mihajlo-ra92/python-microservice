import uuid
from typing import Optional, Union
from logging import Logger
from flask_mysqldb import MySQL
from user_model import User


class UserRepo(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.mysql = mysql
        self.logger = logger

    def read_all(self) -> list[User]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT id, username, email, user_type FROM Users")
        return zip_data(cur)

    def read_by_id(self, user_id) -> Optional[User]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Users WHERE id='{user_id}';")
        users = zip_data(cur)
        if len(users) > 0:
            return users[0]
        return None

    def read_by_username(self, username) -> Optional[User]:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Users WHERE username='{username}';")
        users = zip_data(cur)
        if len(users) > 0:
            return users[0]
        return None

    def create(self, user: User) -> Union[Exception, User]:
        user.id = str(uuid.uuid1())
        cur = self.mysql.connection.cursor()
        try:
            cur.execute(
                f"INSERT INTO Users(id, username, password, email, user_type) VALUES \
                ('{user.id}', '{user.username}', '{user.password}', '{user.email}', '{user.user_type}');"
            )
        except Exception as ex:
            self.logger.info(ex)
            return ex
        self.mysql.connection.commit()
        cur.close()
        return user

    def update(self, user: User) -> User:
        cur = self.mysql.connection.cursor()
        cur.execute(
            f"UPDATE  Users \
                    SET username = '{user.username}', password = '{user.password}', email = '{user.email}' \
                    WHERE id = '{user.id}';"
        )
        self.mysql.connection.commit()
        cur.close()
        return user

    def delete_by_id(self, user_id: str) -> bool:
        cur = self.mysql.connection.cursor()
        cur.execute(f"DELETE FROM Users WHERE id='{user_id}';")
        self.mysql.connection.commit()
        cur.close()
        return True


def zip_data(cur) -> list[User]:
    row_headers = [x[0] for x in cur.description]
    retVal = cur.fetchall()
    cur.close()
    json_data = []
    for result in retVal:
        json_data.append(dict(zip(row_headers, result)))
    users: list[User] = json_data
    return users
