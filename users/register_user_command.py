import uuid
from dataclasses import dataclass, field

from users.password import Password
from users.user_name import UserName


@dataclass(frozen=True)
class RegisterUser:
    username: UserName
    password: Password
    about: str
    ID: uuid = field(default_factory=uuid.uuid4)
