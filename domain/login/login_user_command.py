from dataclasses import dataclass

from domain.users.password import Password
from domain.users.user_name import UserName


@dataclass(frozen=True)
class LoginUser:
    username: UserName
    password: Password
