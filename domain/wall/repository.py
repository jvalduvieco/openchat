import abc
from typing import List

from domain.posts.post import Post
from domain.posts.post_created import PostCreated
from domain.users.user_id import UserID


class WallRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user_id: UserID, event: PostCreated) -> None:
        pass

    @abc.abstractmethod
    def by_user_id(self, user_id: UserID) -> List[Post]:
        pass
