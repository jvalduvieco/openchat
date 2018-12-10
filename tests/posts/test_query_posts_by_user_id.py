from unittest import TestCase

from infrastructure.posts.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from posts.posts_by_user_id_query import PostsByUserID
from posts.query_posts_by_user_id import QueryPostByUserID
from tests.fixtures.posts import a_post_by_maria
from tests.fixtures.users import maria
from users.query_user_by_id import QueryUserByID


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
