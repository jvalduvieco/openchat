from unittest import TestCase

from domain.services.query_user_by_username import QueryUserByUserName
from domain.users.exceptions import DuplicatedUserName
from domain.users.services import UserRegistrator
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.users import create_maria, maria


class TestRegisterUser(TestCase):
    def test_should_register_a_new_user(self):
        command = create_maria()
        user_registrator = UserRegistrator(QueryUserByUserName(InMemoryUsersRepository()))

        (a_registered_user, events) = user_registrator.execute(command)

        self.assertEqual(command.username, a_registered_user.username)
        self.assertEqual(1, len(events))
        self.assertEqual(command.username, events[0].username)
        self.assertEqual(command.password, events[0].password)
        self.assertEqual(command.ID, events[0].ID)

    def test_should_throw_an_exception_on_duplicate_username(self):
        user_registrator = UserRegistrator(QueryUserByUserName(InMemoryUsersRepository([maria()])))

        with self.assertRaises(DuplicatedUserName):
            user_registrator.execute(create_maria())
