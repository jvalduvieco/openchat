from typing import List

from users.user import User
from users.user_name import UserName
from users.users_repository import UsersRepository


class InMemoryUsersRepository(UsersRepository):
    users_by_username: {}

    def __init__(self, initial_users: List[User] = []):
        self.users_by_username = {user.username.contents: user for user in initial_users}

    def by_username(self, username: UserName) -> User:
        return self.users_by_username.get(username.contents, None)

    def save(self, user: User) -> None:
        self.users_by_username[user.username.contents] = user
