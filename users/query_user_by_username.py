from users.user import User
from users.user_name import UserName
from users.users_repository import UsersRepository


class QueryUserByUserName(object):
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self, user_name: UserName) -> User:
        return self.user_repository.by_username(user_name)
