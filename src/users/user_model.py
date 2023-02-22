from dataclasses import dataclass


class User(object):
    def __init__(
        self, id: str, username: str, password: str, email: str, user_type: str
    ):
        self.id: str = id
        self.username: str = username
        self.password: str = password
        self.email: str = email
        # TODO: change from str to UserType
        self.user_type: str = user_type


# TODO: Implement enum
# class UserType(Enum):
#     worker = "WORKER"
#     employer = "EMPLOYER"
#     admin = "ADMIN"


@dataclass
class UserData:
    username: str
    user_type: str
