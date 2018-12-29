from dataclasses import dataclass
from datetime import datetime

from domain.users.user_id import UserID


@dataclass(frozen=True)
class RelationshipCreated:
    follower_id: UserID
    followee_id: UserID
    timestamp: datetime
