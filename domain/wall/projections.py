from injector import inject

from domain.posts.events import PostCreated
from domain.relationship.services import QueryRelationshipsByFolloweeID
from domain.wall.adapters import WallRepository


class WallProjection(object):
    @inject
    def __init__(self, wall_repository: WallRepository,
                 query_relationships_by_followee_id: QueryRelationshipsByFolloweeID):
        self.wall_repository = wall_repository
        self.query_relationships_by_followee_id = query_relationships_by_followee_id

    def handle(self, event: PostCreated):
        for relationship in self.query_relationships_by_followee_id.execute(event.user_id):
            self.wall_repository.save(relationship.follower_id, event)
        self.wall_repository.save(event.user_id, event)
