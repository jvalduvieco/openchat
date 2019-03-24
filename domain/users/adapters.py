import abc
from typing import List

from domain.users.user import User
from domain.users.value_objects import UserID, UserName


class UsersRepository(abc.ABC):
    @abc.abstractmethod
    def by_username(self, username: UserName) -> User:
        pass

    @abc.abstractmethod
    def by_id(self, user_id: UserID) -> User:
        pass

    @abc.abstractmethod
    def save(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def all(self) -> List[User]:
        pass
