import abc
from typing import List

from domain.relationship.relationship import Relationship
from domain.users.user_id import UserID


class RelationshipRepository(abc.ABC):
    @abc.abstractmethod
    def by_followee_id(self, followee_id: UserID) -> List[UserID]:
        pass

    @abc.abstractmethod
    def save(self, relationship: Relationship) -> None:
        pass
