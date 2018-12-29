from typing import List

from domain.users.user import User
from domain.users.users_repository import UsersRepository


class QueryAllUsers(object):
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        return self.user_repository.all()
