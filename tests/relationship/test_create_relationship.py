from unittest import TestCase

from domain.relationship.create_relationship import CreateRelationship
from domain.relationship.relationship_creator import RelationshipCreator
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from infrastructure.clock.fake_clock import FakeClock
from infrastructure.repositories.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.users import maria, bob, inexistent_user_id
from domain.users.user_id import UserID


class TestCreateRelationship(TestCase):
    def test_should_create_a_relationsip_from_two_valid_users(self):
        command = CreateRelationship(follower_id=bob().ID, followee_id=maria().ID)
        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])),
                                                   FakeClock(a_perfect_day_and_time()))

        new_relationship, events = relationship_creator.execute(command)

        assert command.follower_id == new_relationship.follower_id
        assert command.followee_id == new_relationship.followee_id
        assert len(events) == 1
        assert events[0].follower_id == command.follower_id
        assert events[0].followee_id == command.followee_id
        assert events[0].timestamp == a_perfect_day_and_time()

    def test_should_throw_an_exception_on_duplicate_username(self):
        command = CreateRelationship(follower_id=UserID(inexistent_user_id()), followee_id=maria().ID)

        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])),
                                                           FakeClock(a_perfect_day_and_time()))

        with self.assertRaises(UnknownUser):
            relationship_creator.execute(command)
