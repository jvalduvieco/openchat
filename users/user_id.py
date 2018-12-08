import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserID:
    contents: uuid = field(default_factory=uuid.uuid4)
