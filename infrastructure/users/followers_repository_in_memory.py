from typing import List

from users.relationship import Relationship
from users.followers_repository import FollowersRepository
from users.user_id import UserID


class InMemoryFollowersRepository(FollowersRepository):
    def __init__(self, initial_relationships=None):
        if initial_relationships is None:
            initial_relationships = []
        self._by_followee_id = {}
        for relationship in initial_relationships:
            self.save(relationship)

    def by_followee_id(self, followee_id: UserID) -> List[UserID]:
        return self._by_followee_id.get(followee_id.contents, [])

    def save(self, relationship: Relationship):
        followers = self._by_followee_id.get(relationship.followee_id.contents, [])
        followers.append(relationship.follower_id)
        self._by_followee_id[relationship.followee_id.contents] = followers
