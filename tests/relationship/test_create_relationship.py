from unittest import TestCase

from domain.relationship.create_relationship import CreateRelationship
from domain.relationship.relationship_creator import RelationshipCreator
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from domain.users.user_id import UserID
from infrastructure.clock.fake_clock import FakeClock
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.users import maria, bob, inexistent_user_id


class TestCreateRelationship(TestCase):
    def test_should_create_a_relationsip_from_two_valid_users(self):
        command = CreateRelationship(follower_id=bob().ID, followee_id=maria().ID)
        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])),
                                                   FakeClock(a_perfect_day_and_time()))

        new_relationship, events = relationship_creator.execute(command)

        self.assertEqual(command.follower_id, new_relationship.follower_id)
        self.assertEqual(command.followee_id, new_relationship.followee_id)
        self.assertEqual(1, len(events))
        self.assertEqual(command.follower_id, events[0].follower_id)
        self.assertEqual(command.followee_id, events[0].followee_id)
        self.assertEqual(a_perfect_day_and_time(), events[0].timestamp)

    def test_should_throw_an_exception_on_inexistent_follower(self):
        command = CreateRelationship(follower_id=UserID(inexistent_user_id()), followee_id=maria().ID)

        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])),
                                                   FakeClock(a_perfect_day_and_time()))

        with self.assertRaises(UnknownUser):
            relationship_creator.execute(command)

    def test_should_throw_an_exception_on_inexistent_followee(self):
        command = CreateRelationship(follower_id=maria().ID, followee_id=UserID(inexistent_user_id()))

        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])),
                                                   FakeClock(a_perfect_day_and_time()))

        with self.assertRaises(UnknownUser):
            relationship_creator.execute(command)
