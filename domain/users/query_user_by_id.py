from domain.users.user_id import UserID
from domain.users.users_repository import UsersRepository


class QueryUserByID(object):
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UserID):
        return self.user_repository.by_id(user_id)
