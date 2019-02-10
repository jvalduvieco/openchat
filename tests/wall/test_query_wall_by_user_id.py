from unittest import TestCase

from domain.posts.post import post_in
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from domain.wall.by_user_id import WallByUserID
from domain.wall.query_wall_by_user_id import QueryWallByUserID
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from infrastructure.repositories.wall_repository_in_memory import InMemoryWallRepository
from tests.fixtures.posts import maria_created_a_post
from tests.fixtures.users import maria, inexistent_user_id


class TestQueryWallByUserID(TestCase):
    def test_should_query_wall_of_a_given_user(self):
        event = maria_created_a_post()
        query = QueryWallByUserID(QueryUserByID(InMemoryUsersRepository([maria()])),
                                  InMemoryWallRepository([(maria().ID, [event])]))
        assert 1 == len(query.execute(WallByUserID(maria().ID)))
        assert post_in(event) == query.execute(WallByUserID(maria().ID))[0]

    def test_should_throw_an_exception_if_user_does_not_exist(self):
        event = maria_created_a_post()
        query = QueryWallByUserID(QueryUserByID(InMemoryUsersRepository([maria()])),
                                  InMemoryWallRepository([(maria().ID, [event])]))
        with self.assertRaises(UnknownUser):
            query.execute(WallByUserID(inexistent_user_id()))
