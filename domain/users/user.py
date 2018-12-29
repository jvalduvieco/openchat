from dataclasses import dataclass

from domain.users.password import Password
from domain.users.user_id import UserID
from domain.users.user_name import UserName


@dataclass(frozen=True)
class User:
    username: UserName
    password: Password
    about: str
    ID: UserID = UserID()
