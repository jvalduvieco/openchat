from dataclasses import dataclass


@dataclass(frozen=True)
class UserName:
    contents: str

    def __post_init__(self):
        if ' ' in self.contents:
            raise ValueError('Spaces not allowed in username')
