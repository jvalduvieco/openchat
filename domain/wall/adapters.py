import abc
from typing import List

from domain.posts.events import PostCreated
from domain.posts.post import Post
from domain.users.value_objects import UserID


class WallRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, user_id: UserID, event: PostCreated) -> None:
        pass

    @abc.abstractmethod
    def by_user_id(self, user_id: UserID) -> List[Post]:
        pass
