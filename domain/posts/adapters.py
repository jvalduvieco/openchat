import abc
from typing import List

from domain.posts.post import Post
from domain.users.value_objects import UserID


class PostsRepository(abc.ABC):
    @abc.abstractmethod
    def by_user_id(self, user_id: UserID) -> List[Post]:
        pass

    @abc.abstractmethod
    def save(self, post: Post) -> None:
        pass
