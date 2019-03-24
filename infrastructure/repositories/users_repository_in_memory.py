from typing import List

from domain.users.adapters import UsersRepository
from domain.users.user import User
from domain.users.value_objects import UserID, UserName


class InMemoryUsersRepository(UsersRepository):
    def __init__(self, initial_users=None):
        if initial_users is None:
            initial_users = []
        self.users_by_username = {}
        self.users_by_id = {}
        for user in initial_users:
            self.save(user)

    def by_username(self, username: UserName) -> User:
        return self.users_by_username.get(username.contents, None)

    def by_id(self, user_id: UserID) -> User:
        return self.users_by_id.get(user_id.contents.__str__(), None)

    def save(self, user: User) -> None:
        self.users_by_username[user.username.contents] = user
        self.users_by_id[user.ID.contents.__str__()] = user

    def all(self) -> List[User]:
        return [user for (key, user) in self.users_by_id.items()]
