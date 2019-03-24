import datetime
from dataclasses import dataclass
from typing import Union

from domain.posts.commands import CreatePost
from domain.posts.events import PostCreated
from domain.posts.value_objects import PostID
from domain.users.value_objects import UserID


@dataclass(frozen=True)
class Post:
    post_id: PostID
    user_id: UserID
    text: str
    created_at: datetime


def post_in(subject: Union[CreatePost, PostCreated]) -> Post:
    return Post(user_id=subject.user_id, post_id=subject.post_id, text=subject.text, created_at=subject.created_at)
