from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ApplicationStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApplicationDecision(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass
class Application:
    id: str = ""
    worker_id: str = ""
    worker = None
    job_id: str = ""
    job = None
    description: str = ""
    status: ApplicationStatus = ApplicationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def toJSON(self):
        return json.dumps(self, default=self._json_default, sort_keys=True, indent=4)

    def _json_default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.name
        raise TypeError("Type not serializable")


@dataclass
class UserData:
    username: str
    user_type: str


class MyException(Exception):
    pass
