from unittest import TestCase

from domain.users.services import QueryAllUsers
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.users import maria, bob


class TestQueryAllUsers(TestCase):
    def test_should_query_all_users(self):
        query_all_users = QueryAllUsers(InMemoryUsersRepository([bob(), maria()]))

        all_users = query_all_users.execute()

        self.assertEqual(2, len(all_users))
        self.assertIn(maria(), all_users)
        self.assertIn(bob(), all_users)
