from dataclasses import dataclass

from users.user_id import UserID


@dataclass(frozen=True)
class WallByUserID(object):
    user_id: UserID
