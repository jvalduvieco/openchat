import datetime
from dataclasses import dataclass

from domain.posts.value_objects import PostID
from domain.users.value_objects import UserID


@dataclass(frozen=True)
class CreatePost:
    post_id: PostID
    user_id: UserID
    text: str
    created_at: datetime
