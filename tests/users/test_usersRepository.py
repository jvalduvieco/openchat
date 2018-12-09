from unittest import TestCase

from parameterized import parameterized

from tests.fixtures.user import maria
from users.users_repository import UsersRepository
from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository


class TestUsersRepository(TestCase):
    @parameterized.expand([
        [InMemoryUsersRepository()]
    ])
    def test_should_save_a_user_and_recover(self, user_repository: UsersRepository):
        a_user = maria()
        user_repository.save(a_user)
        user_from_repo = user_repository.by_username(a_user.username)
        assert a_user == user_from_repo
