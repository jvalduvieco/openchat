from dataclasses import dataclass

from domain.users.value_objects import UserID


@dataclass(frozen=True)
class Relationship:
    followee_id: UserID
    follower_id: UserID
