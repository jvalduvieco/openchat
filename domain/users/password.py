from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    contents: str

    def __post_init__(self):
        if ' ' in self.contents:
            raise ValueError('Spaces not allowed in passwords')
