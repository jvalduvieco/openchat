import abc
from dataclasses import dataclass
from typing import List
from unittest import TestCase

from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from posts.post import Post
from posts.post_id import PostID
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.user import maria
from users.exceptions import UnkownUser
from users.query_user_by_id import QueryUserByID
from users.user_id import UserID


@dataclass(frozen=True)
class PostsByUserID:
    user_id: UserID


class PostsRepository(abc.ABC):
    @abc.abstractmethod
    def by_user_id(self, user_id: UserID) -> List[Post]:
        pass

    @abc.abstractmethod
    def save(self, post: Post) -> None:
        pass


class InMemoryPostsRepository(PostsRepository):
    def __init__(self, initial_posts=None):
        if initial_posts is None:
            initial_posts = []
        self.posts_by_user_id = {}
        for post in initial_posts:
            self.save(post)

    def by_user_id(self, user_id: UserID) -> List[Post]:
        return self.posts_by_user_id.get(user_id.contents, [])

    def save(self, post: Post) -> None:
        current_posts = self.posts_by_user_id.get(post.user_id.contents, [])
        current_posts.append(post)
        self.posts_by_user_id[post.user_id.contents] = current_posts


class QueryPostByUserID(object):
    def __init__(self, query_users_by_id: QueryUserByID, posts_repository: PostsRepository):
        self.query_users_by_id = query_users_by_id
        self.posts_repository = posts_repository

    def execute(self, query) -> List[Post]:
        user = self.query_users_by_id.execute(query.user_id)
        if user is None:
            raise UnkownUser('User %s does not exist' % query.user_id.contents)
        return self.posts_repository.by_user_id(query.user_id)


def a_post_by_maria():
    return Post(PostID('116c6055-86fe-4335-a332-5a586e995c12'), maria().ID, 'Hi! this is Maria',
                a_perfect_day_and_time())


class TestCreatePost(TestCase):
    def test_should_get_a_list_of_posts_by_user_id(self):
        query = PostsByUserID(user_id=maria().ID)
        posts_by_user_id = QueryPostByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria()]))
        post_list = posts_by_user_id.execute(query)
        assert len(post_list) == 1
