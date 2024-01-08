from dataclasses import dataclass
import json


class Application(object):
    def __init__(
        self,
        id: str = "",
        worker_id: str = "",
        job_id: str = "",
        description: str = "",
        # TODO: Implement created_at
    ):
        self.id: str = id
        self.worker_id: str = worker_id
        self.job_id: str = job_id
        self.description: str = description

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@dataclass
class UserData:
    username: str
    user_type: str


class MyException(Exception):
    pass
