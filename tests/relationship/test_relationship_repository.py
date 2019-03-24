from unittest import TestCase

from parameterized import parameterized

from domain.relationship.adapters import RelationshipRepository
from infrastructure.repositories.relationship_repository_in_memory import InMemoryRelationshipRepository
from tests.fixtures.users import bob_follows_maria


class TestRelationshipRepository(TestCase):
    @parameterized.expand([
        [InMemoryRelationshipRepository()]
    ])
    def test_should_save_a_relationship_and_recover_by_followee(self, followers_repository: RelationshipRepository):
        a_relationship = bob_follows_maria()
        followers_repository.save(a_relationship)

        relationships = followers_repository.by_followee_id(a_relationship.followee_id)

        self.assertIn(a_relationship, relationships)

    @parameterized.expand([
        [InMemoryRelationshipRepository()]
    ])
    def test_should_save_a_relationship_and_recover_by_follower(self, followers_repository: RelationshipRepository):
        a_relationship = bob_follows_maria()
        followers_repository.save(a_relationship)

        relationships = followers_repository.by_follower_id(a_relationship.follower_id)

        self.assertIn(a_relationship, relationships)
