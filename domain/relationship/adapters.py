import abc
from typing import List

from domain.relationship.relationship import Relationship
from domain.users.value_objects import UserID


class RelationshipRepository(abc.ABC):
    @abc.abstractmethod
    def by_follower_id(self, followee_id: UserID) -> List[Relationship]:
        pass

    @abc.abstractmethod
    def by_followee_id(self, followee_id: UserID) -> List[Relationship]:
        pass

    @abc.abstractmethod
    def save(self, relationship: Relationship) -> None:
        pass
