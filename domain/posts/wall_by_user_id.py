from dataclasses import dataclass

from domain.users.user_id import UserID


@dataclass(frozen=True)
class WallByUserID(object):
    user_id: UserID
