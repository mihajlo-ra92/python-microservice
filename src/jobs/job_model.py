from dataclasses import dataclass
import json


class Job(object):
    def __init__(
        self,
        id: str = "",
        employer_id: str = "",
        worker_id: str = "",
        job_name: str = "",
        job_desc: str = "",
        pay_in_euro: float = 0.0,
        completed: bool = False,
    ):
        self.id: str = id
        self.employer_id: str = employer_id
        self.worker_id: str = worker_id
        self.job_name: str = job_name
        self.job_desc: str = job_desc
        self.pay_in_euro: float = pay_in_euro
        self.completed: bool = completed

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@dataclass
class UserData:
    username: str
    user_type: str


class MyException(Exception):
    pass
