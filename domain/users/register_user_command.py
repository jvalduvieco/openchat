import uuid
from dataclasses import dataclass, field

from domain.users.password import Password
from domain.users.user_name import UserName


@dataclass(frozen=True)
class RegisterUser:
    username: UserName
    password: Password
    about: str
    ID: uuid = field(default_factory=uuid.uuid4)
