from unittest import TestCase

from parameterized import parameterized

from infrastructure.repositories.users.followers_repository_in_memory import InMemoryFollowersRepository
from tests.fixtures.users import bob_follows_maria
from users.followers_repository import FollowersRepository


class TestRelationshipRepository(TestCase):
    @parameterized.expand([
        [InMemoryFollowersRepository()]
    ])
    def test_should_save_a_relationship_and_recover_by_followee(self, followers_repository: FollowersRepository):
        a_relationship = bob_follows_maria()
        followers_repository.save(a_relationship)

        followers = followers_repository.by_followee_id(a_relationship.followee_id)

        assert 1 == len(followers)
        assert a_relationship.follower_id == followers[0]
