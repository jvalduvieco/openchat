from dataclasses import dataclass

from users.password import Password
from users.user_name import UserName


@dataclass(frozen=True)
class LoginUser:
    username: UserName
    password: Password
