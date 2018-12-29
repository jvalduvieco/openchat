import datetime
from dataclasses import dataclass
from users.user_name import UserName


@dataclass(frozen=True)
class UserSignedIn:
    username: UserName
    timestamp: datetime

