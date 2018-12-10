from dataclasses import dataclass

from users.user_id import UserID


@dataclass(frozen=True)
class PostsByUserID:
    user_id: UserID
