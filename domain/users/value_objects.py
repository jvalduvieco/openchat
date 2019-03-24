import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Password:
    contents: str

    def __post_init__(self):
        if type(self.contents) is not str:
            raise ValueError('Password must be a string')
        elif ' ' in self.contents:
            raise ValueError('Spaces not allowed in passwords')
        elif len(self.contents) == 0:
            raise ValueError('Password can not be empty')


@dataclass(frozen=True)
class UserID:
    contents: uuid = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class UserName:
    contents: str

    def __post_init__(self):
        if type(self.contents) is not str:
            raise ValueError('UserName must be a string')
        elif ' ' in self.contents:
            raise ValueError('Spaces not allowed in username')
        elif len(self.contents) == 0:
            raise ValueError('UserName can not be empty')
