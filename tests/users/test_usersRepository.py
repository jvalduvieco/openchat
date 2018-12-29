from unittest import TestCase

from parameterized import parameterized

from infrastructure.repositories.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.users import maria
from users.users_repository import UsersRepository


class TestUsersRepository(TestCase):
    @parameterized.expand([
        [InMemoryUsersRepository()]
    ])
    def test_should_save_a_user_and_recover_by_username(self, user_repository: UsersRepository):
        a_user = maria()
        user_repository.save(a_user)

        user_from_repo = user_repository.by_username(a_user.username)

        assert a_user == user_from_repo

    @parameterized.expand([
        [InMemoryUsersRepository()]
    ])
    def test_should_save_a_user_and_recover_by_user_id(self, user_repository: UsersRepository):
        a_user = maria()
        user_repository.save(a_user)

        user_from_repo = user_repository.by_id(a_user.ID)

        assert a_user == user_from_repo
