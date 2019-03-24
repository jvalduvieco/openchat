from dataclasses import dataclass

from domain.users.value_objects import UserID


@dataclass(frozen=True)
class CreateRelationship:
    follower_id: UserID
    followee_id: UserID
