import json, uuid
from logging import Logger
from flask_mysqldb import MySQL
from user_model import User


class UserRepo(object):
    def __init__(self, mysql: MySQL, logger: Logger):
        self.mysql = mysql
        self.logger = logger

    def read_all(self) -> list[User]:
        self.logger.info("!!! FROM REPO !!!")
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Users")
        row_headers = [x[0] for x in cur.description]
        retVal = cur.fetchall()
        cur.close()
        json_data = []
        for result in retVal:
            json_data.append(dict(zip(row_headers, result)))
        users: list[User] = json_data
        return users

    def read_by_id(self, user_id) -> User:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Users WHERE id='{user_id}';")
        row_headers = [x[0] for x in cur.description]
        retVal = cur.fetchall()
        cur.close()
        json_data = []

        for result in retVal:
            json_data.append(dict(zip(row_headers, result)))
        users: list[User] = json_data
        return users[0]

    def read_by_username(self, username) -> User:
        cur = self.mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Users WHERE username='{username}';")
        row_headers = [x[0] for x in cur.description]
        retVal = cur.fetchall()
        cur.close()
        json_data = []

        for result in retVal:
            json_data.append(dict(zip(row_headers, result)))
        users: list[User] = json_data
        return users[0]

    def create(self, user: User) -> User:
        user["id"] = str(uuid.uuid1())
        cur = self.mysql.connection.cursor()
        cur.execute(
            f"INSERT INTO Users(id, username, password, email, user_type) VALUES \
            ('{user['id']}', '{user['username']}', '{user['password']}', '{user['email']}', '{user['user_type']}');"
        )
        self.mysql.connection.commit()
        cur.close()
        return user

    def update(self, user: User) -> User:
        cur = self.mysql.connection.cursor()
        cur.execute(
            f"UPDATE  Users \
                    SET username = '{user['username']}', password = '{user['password']}', email = '{user['email']}' \
                    WHERE id = '{user['id']}';"
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
