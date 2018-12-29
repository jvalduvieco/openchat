from typing import Tuple, List

from misc.clock import Clock
from users.exceptions import UnknownUser
from users.query_user_by_id import QueryUserByID
from users.relationship import Relationship
from users.relationship_created import RelationshipCreated


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
