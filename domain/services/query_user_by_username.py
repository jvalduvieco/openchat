from injector import inject

from domain.users.adapters import UsersRepository
from domain.users.user import User
from domain.users.value_objects import UserName


class QueryUserByUserName(object):
    @inject
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self, user_name: UserName) -> User:
        return self.user_repository.by_username(user_name)
