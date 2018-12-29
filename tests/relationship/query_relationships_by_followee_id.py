from tests.relationship.relationship_repository import RelationshipRepository
from users.user_id import UserID


class QueryFollowersByFolloweeID(object):
    def __init__(self, relationship_repository: RelationshipRepository):
        self.relationship_repository = relationship_repository

    def execute(self, user_id: UserID):
        return self.relationship_repository.by_followee_id(user_id)
