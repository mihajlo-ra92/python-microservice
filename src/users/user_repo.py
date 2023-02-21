import json, uuid
from flask_mysqldb import MySQL
from user_model import User


class UserRepo(object):
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def read_all(self) -> list[User]:
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

    def read_user(self, user_id) -> User:
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

    def create_user(self, user: User) -> User:
        user["id"] = str(uuid.uuid1())
        cur = self.mysql.connection.cursor()
        cur.execute(
            f"INSERT INTO Users(id, username, password, email, user_type) VALUES \
            ('{user['id']}', '{user['username']}', '{user['password']}', '{user['email']}', '{user['user_type']}');"
        )
        self.mysql.connection.commit()
        cur.close()
        return user
