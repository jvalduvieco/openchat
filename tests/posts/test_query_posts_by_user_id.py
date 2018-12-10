from unittest import TestCase

from infrastructure.posts.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from posts.posts_by_user_id_query import PostsByUserID
from posts.query_posts_by_user_id import QueryPostByUserID
from tests.fixtures.posts import a_post_by_maria, another_post_by_maria
from tests.fixtures.users import maria
from users.exceptions import UnknownUser
from users.query_user_by_id import QueryUserByID
from users.user_id import UserID


class TestCreatePost(TestCase):
    def test_should_get_a_list_of_posts_by_user_id(self):
        query = PostsByUserID(user_id=maria().ID)
        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria()]))
        post_list = posts_by_user_id.execute(query)
        assert 1 == len(post_list)
        assert a_post_by_maria().post_id == post_list[0].post_id
        assert a_post_by_maria().user_id == post_list[0].user_id

    def test_should_get_a_list_of_posts_by_user_id_multiple_posts(self):
        query = PostsByUserID(user_id=maria().ID)
        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), another_post_by_maria()]))
        post_list = posts_by_user_id.execute(query)
        assert 2 == len(post_list)
        assert a_post_by_maria().post_id == post_list[0].post_id
        assert another_post_by_maria().post_id == post_list[1].post_id

    def test_shoul_throw_an_exception_if_user_does_not_exist(self):
        query = PostsByUserID(user_id=UserID('deabeef-7fe9-47b6-a138-42e81deabeef'))
        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria()]))
        with self.assertRaises(UnknownUser):
            posts_by_user_id.execute(query)
