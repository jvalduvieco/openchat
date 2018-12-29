from typing import List, Tuple

from domain.misc.clock import Clock
from domain.relationship.relationship import Relationship
from domain.relationship.relationship_created import RelationshipCreated
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID


class RelationshipCreator(object):
    def __init__(self, query_user_by_id: QueryUserByID, clock: Clock):
        self.clock = clock
        self.query_user_by_id = query_user_by_id

    def execute(self, command) -> Tuple[Relationship, List[RelationshipCreated]]:
        if self.query_user_by_id.execute(command.follower_id) is None:
            raise UnknownUser('User with id: %d not found')
        if self.query_user_by_id.execute(command.followee_id) is None:
            raise UnknownUser('User with id: %d not found')
        return Relationship(followee_id=command.followee_id, follower_id=command.follower_id), \
               [RelationshipCreated(followee_id=command.followee_id, follower_id=command.follower_id,
                                    timestamp=self.clock.now())]
