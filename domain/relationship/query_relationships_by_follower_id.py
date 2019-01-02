from injector import inject

from domain.relationship.relationship_repository import RelationshipRepository
from domain.users.user_id import UserID


class QueryRelationshipsByFollowerID(object):
    @inject
    def __init__(self, relationship_repository: RelationshipRepository):
        self.relationship_repository = relationship_repository

    def execute(self, user_id: UserID):
        return self.relationship_repository.by_follower_id(user_id)
