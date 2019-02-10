from unittest import TestCase

from domain.relationship.query_relationships_by_followee_id import QueryRelationshipsByFolloweeID
from domain.wall.projection import WallProjection
from infrastructure.repositories.relationship_repository_in_memory import InMemoryRelationshipRepository
from infrastructure.repositories.wall_repository_in_memory import InMemoryWallRepository
from tests.fixtures.posts import maria_created_a_post
from tests.fixtures.users import maria, bob_follows_maria, bob


class TestWall(TestCase):
    def test_should_see_own_posts_on_wall(self):
        wall_repository = InMemoryWallRepository()
        wall_projection = WallProjection(
            wall_repository=wall_repository,
            query_relationships_by_followee_id=QueryRelationshipsByFolloweeID(
                InMemoryRelationshipRepository([bob_follows_maria()])))

        wall_projection.handle(maria_created_a_post())

        assert 1 == len(wall_repository.by_user_id(maria().ID))

    def test_should_see_followee_posts_on_follower_wall(self):
        wall_repository = InMemoryWallRepository()
        wall_projection = WallProjection(
            wall_repository=wall_repository,
            query_relationships_by_followee_id=QueryRelationshipsByFolloweeID(
                InMemoryRelationshipRepository([bob_follows_maria()])))

        wall_projection.handle(maria_created_a_post())

        assert 1 == len(wall_repository.by_user_id(bob().ID))
