import datetime
import uuid
from dataclasses import dataclass, field
from unittest import TestCase

from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.user import maria
from users.user_id import UserID
from users.users_repository import UsersRepository


@dataclass(frozen=True)
class PostID:
    contents: uuid = field(default_factory=uuid.uuid4)


def a_perfect_day_and_time() -> datetime:
    return datetime.datetime(2020, 5, 17, 15, 15, 0)


@dataclass(frozen=True)
class CreatePost:
    post_id: PostID
    user_id: UserID
    text: str
    created_at: datetime


class QueryUserByID(object):
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UserID):
        return self.user_repository.by_id(user_id)


@dataclass(frozen=True)
class Post:
    post_id: PostID
    user_id: UserID
    text: str
    created_at: datetime


class PostCreator(object):
    def __init__(self, query_user_by_id: QueryUserByID):
        self.query_user_by_id = query_user_by_id

    def execute(self, command: CreatePost):
        user = self.query_user_by_id.execute(command.user_id)
        if user is not None:
            return Post(post_id=command.post_id,
                        user_id=command.user_id,
                        text=command.text,
                        created_at=command.created_at)


class TestCreatePost(TestCase):
    def test_should_create_a_post(self):
        command = CreatePost(post_id=PostID(), user_id=maria().ID, text='', created_at=a_perfect_day_and_time())
        post_creator = PostCreator(QueryUserByID(InMemoryUsersRepository([maria()])))
        created_post = post_creator.execute(command)
        assert command.post_id == created_post.post_id
        assert command.user_id == created_post.user_id
        assert command.text == created_post.text
        assert command.created_at == created_post.created_at
