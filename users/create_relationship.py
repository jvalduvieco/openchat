from dataclasses import dataclass

from users.user_id import UserID


@dataclass(frozen=True)
class CreateRelationship:
    follower_id: UserID
    followee_id: UserID
