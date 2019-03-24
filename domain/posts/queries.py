from dataclasses import dataclass

from domain.users.value_objects import UserID


@dataclass(frozen=True)
class PostsByUserID:
    user_id: UserID
