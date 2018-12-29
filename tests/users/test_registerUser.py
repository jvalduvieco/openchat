from unittest import TestCase

from infrastructure.repositories.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.users import create_maria, maria
from users.query_user_by_username import QueryUserByUserName
from users.user_registrator import UserRegistrator, DuplicatedUserName


class TestRegisterUser(TestCase):
    def test_should_register_a_new_user(self):
        command = create_maria()
        user_registrator = UserRegistrator(QueryUserByUserName(InMemoryUsersRepository()))

        (a_registered_user, events) = user_registrator.execute(command)

        assert a_registered_user.username == command.username
        assert len(events) == 1
        assert events[0].username == command.username
        assert events[0].password == command.password
        assert events[0].ID == command.ID

    def test_should_throw_an_exception_on_duplicate_username(self):
        user_registrator = UserRegistrator(QueryUserByUserName(InMemoryUsersRepository([maria()])))

        with self.assertRaises(DuplicatedUserName):
            user_registrator.execute(create_maria())
