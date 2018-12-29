import datetime
from dataclasses import dataclass

from domain.posts.post_id import PostID
from domain.users.user_id import UserID


@dataclass(frozen=True)
class CreatePost:
    post_id: PostID
    user_id: UserID
    text: str
    created_at: datetime
