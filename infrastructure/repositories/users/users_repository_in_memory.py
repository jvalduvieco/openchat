from domain.users.user import User
from domain.users.user_id import UserID
from domain.users.user_name import UserName
from domain.users.users_repository import UsersRepository


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
        return self.users_by_id.get(user_id.contents, None)

    def save(self, user: User) -> None:
        self.users_by_username[user.username.contents] = user
        self.users_by_id[user.ID.contents] = user

    def all(self):
        return [user for (key, user) in self.users_by_id.items()]
