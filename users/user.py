import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class User:
    username: str
    password: str
    about: str
    ID: uuid = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if ' ' in self.username:
            raise ValueError('Spaces not allowed in username')
