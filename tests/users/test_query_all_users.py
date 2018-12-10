from unittest import TestCase

from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.users import maria, bob
from users.query_all_users import QueryAllUsers


class TestQueryAllUsers(TestCase):
    def test_should_query_all_users(self):
        query_all_users = QueryAllUsers(InMemoryUsersRepository([bob(), maria()]))
        all_users = query_all_users.execute()

        assert 2 == len(all_users)
        assert maria() in all_users
        assert bob() in all_users
