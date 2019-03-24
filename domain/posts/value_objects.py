import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PostID:
    contents: uuid = field(default_factory=uuid.uuid4)
