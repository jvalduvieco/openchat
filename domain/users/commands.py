from dataclasses import dataclass

from domain.users.value_objects import Password, UserID, UserName


@dataclass(frozen=True)
class RegisterUser:
    username: UserName
    password: Password
    about: str
    ID: UserID