import datetime
from dataclasses import dataclass

from domain.users.user_name import UserName


@dataclass(frozen=True)
class UserSignedIn:
    username: UserName
    timestamp: datetime
