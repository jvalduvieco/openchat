import datetime
from dataclasses import dataclass

from domain.users.value_objects import UserName


@dataclass(frozen=True)
class UserSignedIn:
    username: UserName
    timestamp: datetime
