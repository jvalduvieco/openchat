import abc
from typing import List

from posts.post import Post
from users.user_id import UserID


class PostsRepository(abc.ABC):
    @abc.abstractmethod
    def by_user_id(self, user_id: UserID) -> List[Post]:
        pass

    @abc.abstractmethod
    def save(self, post: Post) -> None:
        pass
