from dataclasses import dataclass
from unittest import TestCase

from tests.fixtures.users import maria, bob, inexistent_user_id
from users.exceptions import UnknownUser
from users.query_user_by_id import QueryUserByID
from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from users.relationship import Relationship
from users.user_id import UserID


@dataclass(frozen=True)
class CreateRelationship:
    follower_id: UserID
    followee_id: UserID


class RelationshipCreator(object):
    def __init__(self, query_user_by_id: QueryUserByID):
        self.query_user_by_id = query_user_by_id

    def execute(self, command):
        if self.query_user_by_id.execute(command.follower_id) is None:
            raise UnknownUser('User with id: %d not found')
        if self.query_user_by_id.execute(command.followee_id) is None:
            raise UnknownUser('User with id: %d not found')
        return Relationship(followee_id=command.followee_id, follower_id=command.follower_id)


class TestCreateRelationship(TestCase):
    def test_should_create_a_relationsip_from_two_valid_users(self):
        command = CreateRelationship(follower_id=bob().ID, followee_id=maria().ID)
        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])))

        new_relationship = relationship_creator.execute(command)

        assert command.follower_id == new_relationship.follower_id
        assert command.followee_id == new_relationship.followee_id

    def test_should_throw_an_exception_on_duplicate_username(self):
        command = CreateRelationship(follower_id=UserID(inexistent_user_id()), followee_id=maria().ID)
        relationship_creator = RelationshipCreator(QueryUserByID(InMemoryUsersRepository([bob(), maria()])))

        with self.assertRaises(UnknownUser):
            relationship_creator.execute(command)
