from unittest import TestCase

from typing import Union

from domain.posts.create_post_command import CreatePost
from domain.posts.exceptions import UnkownUserID
from domain.posts.post import Post
from domain.posts.post_created import PostCreated
from domain.posts.post_creator import PostCreator
from domain.posts.post_id import PostID
from domain.users.query_user_by_id import QueryUserByID
from domain.users.user_id import UserID
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.users import maria


def post_in(subject: Union[CreatePost, PostCreated]) -> Post:
    return Post(user_id=subject.user_id, post_id=subject.post_id, text=subject.text, created_at=subject.created_at)


class TestCreatePost(TestCase):
    def test_should_create_a_post(self):
        command = CreatePost(post_id=PostID(), user_id=maria().ID, text='', created_at=a_perfect_day_and_time())
        post_creator = PostCreator(QueryUserByID(InMemoryUsersRepository([maria()])))

        created_post, events = post_creator.execute(command)

        assert post_in(command) == created_post
        assert post_in(command) == post_in(events[0])
        assert 1 == len(events)

    def test_should_throw_an_exception_on_inexistent_user(self):
        command = CreatePost(post_id=PostID(),
                             user_id=UserID('fc673127-c5b9-4128-9015-2bbc31163df1'),
                             text='',
                             created_at=a_perfect_day_and_time())

        post_creator = PostCreator(QueryUserByID(InMemoryUsersRepository([maria()])))

        with self.assertRaises(UnkownUserID):
            post_creator.execute(command)
