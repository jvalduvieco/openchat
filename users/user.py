from dataclasses import dataclass

from users.password import Password
from users.user_id import UserID
from users.user_name import UserName


@dataclass(frozen=True)
class User:
    username: UserName
    password: Password
    about: str
    ID: UserID = UserID()
