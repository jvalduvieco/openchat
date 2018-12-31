from unittest import TestCase

from domain.posts.posts_by_user_id_query import PostsByUserID
from domain.posts.query_posts_by_user_id import QueryPostByUserID
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from infrastructure.repositories.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.posts import a_post_by_maria, another_post_by_maria
from tests.fixtures.users import maria, inexistent_user_id


class TestCreatePost(TestCase):
    def test_should_get_a_list_of_posts_by_user_id(self):
        query = PostsByUserID(user_id=maria().ID)
        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria()]))

        post_list = posts_by_user_id.execute(query)

        assert 1 == len(post_list)
        assert a_post_by_maria() in post_list

    def test_should_get_a_list_of_posts_by_user_id_multiple_posts(self):
        query = PostsByUserID(user_id=maria().ID)
        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), another_post_by_maria()]))

        post_list = posts_by_user_id.execute(query)

        assert 2 == len(post_list)
        assert a_post_by_maria() in post_list
        assert another_post_by_maria() in post_list

    def test_shoul_throw_an_exception_if_user_does_not_exist(self):
        query = PostsByUserID(user_id=inexistent_user_id())

        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria()]))

        with self.assertRaises(UnknownUser):
            posts_by_user_id.execute(query)
