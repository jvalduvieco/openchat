from unittest import TestCase

from parameterized import parameterized

from infrastructure.repositories.relationship.relationship_repository_in_memory import InMemoryRelationshipRepository
from tests.fixtures.users import bob_follows_maria
from domain.relationship.relationship_repository import RelationshipRepository


class TestRelationshipRepository(TestCase):
    @parameterized.expand([
        [InMemoryRelationshipRepository()]
    ])
    def test_should_save_a_relationship_and_recover_by_followee(self, followers_repository: RelationshipRepository):
        a_relationship = bob_follows_maria()
        followers_repository.save(a_relationship)

        followers = followers_repository.by_followee_id(a_relationship.followee_id)

        assert 1 == len(followers)
        assert a_relationship.follower_id == followers[0]
