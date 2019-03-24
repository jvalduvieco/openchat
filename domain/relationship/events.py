from dataclasses import dataclass
from datetime import datetime

from domain.users.value_objects import UserID


@dataclass(frozen=True)
class RelationshipCreated:
    follower_id: UserID
    followee_id: UserID
    timestamp: datetime
