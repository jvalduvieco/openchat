from dataclasses import dataclass


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
