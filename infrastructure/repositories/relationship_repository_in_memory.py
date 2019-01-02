from typing import List

from domain.relationship.relationship import Relationship
from domain.relationship.relationship_repository import RelationshipRepository
from domain.users.user_id import UserID


class InMemoryRelationshipRepository(RelationshipRepository):
    def __init__(self, initial_relationships=None):
        if initial_relationships is None:
            initial_relationships = []
        self._by_follower_id = {}
        self._by_followee_id = {}
        for relationship in initial_relationships:
            self.save(relationship)

    def by_follower_id(self, followee_id: UserID) -> List[Relationship]:
        return self._by_follower_id.get(followee_id.contents, [])

    def by_followee_id(self, followee_id: UserID) -> List[Relationship]:
        return self._by_followee_id.get(followee_id.contents, [])

    def save(self, relationship: Relationship):
        by_followee_id = self._by_followee_id.get(relationship.followee_id.contents, [])
        by_follower_id = self._by_follower_id.get(relationship.follower_id.contents, [])
        by_followee_id.append(relationship)
        by_follower_id.append(relationship)
        self._by_followee_id[relationship.followee_id.contents] = by_followee_id
        self._by_follower_id[relationship.follower_id.contents] = by_follower_id
