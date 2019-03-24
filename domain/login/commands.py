from dataclasses import dataclass

from domain.users.value_objects import Password, UserName


@dataclass(frozen=True)
class LoginUser:
    username: UserName
    password: Password
