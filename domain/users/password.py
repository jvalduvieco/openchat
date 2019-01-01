from dataclasses import dataclass


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
