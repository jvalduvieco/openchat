from domain.users.user import User
from domain.users.user_name import UserName
from domain.users.users_repository import UsersRepository


class QueryUserByUserName(object):
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self, user_name: UserName) -> User:
        return self.user_repository.by_username(user_name)
