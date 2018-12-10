import abc
from typing import List

from users.relationship import Relationship
from users.user_id import UserID


class RelationshipsRepository(abc.ABC):
    @abc.abstractmethod
    def by_followee_id(self, followee_id: UserID) -> List[UserID]:
        pass

    @abc.abstractmethod
    def save(self, relationship: Relationship) -> None:
        pass
