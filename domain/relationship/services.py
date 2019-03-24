from typing import Tuple, List

from injector import inject

from domain.misc.clock import Clock
from domain.relationship.adapters import RelationshipRepository
from domain.relationship.events import RelationshipCreated
from domain.relationship.relationship import Relationship
from domain.users.exceptions import UnknownUser
from domain.users.services import QueryUserByID
from domain.users.value_objects import UserID


class QueryRelationshipsByFolloweeID(object):
    @inject
    def __init__(self, relationship_repository: RelationshipRepository):
        self.relationship_repository = relationship_repository

    def execute(self, user_id: UserID):
        return self.relationship_repository.by_followee_id(user_id)


class QueryRelationshipsByFollowerID(object):
    @inject
    def __init__(self, relationship_repository: RelationshipRepository):
        self.relationship_repository = relationship_repository

    def execute(self, user_id: UserID):
        return self.relationship_repository.by_follower_id(user_id)


class RelationshipCreator(object):
    @inject
    def __init__(self, query_user_by_id: QueryUserByID, clock: Clock):
        self.clock = clock
        self.query_user_by_id = query_user_by_id

    def execute(self, command) -> Tuple[Relationship, List[RelationshipCreated]]:
        if self.query_user_by_id.execute(command.follower_id) is None:
            raise UnknownUser('User with id: %d not found')
        if self.query_user_by_id.execute(command.followee_id) is None:
            raise UnknownUser('User with id: %d not found')
        return Relationship(followee_id=command.followee_id, follower_id=command.follower_id), [
            RelationshipCreated(followee_id=command.followee_id, follower_id=command.follower_id,
                                timestamp=self.clock.now())]
