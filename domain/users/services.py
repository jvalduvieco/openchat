from typing import List, Tuple

from injector import inject

from domain.services.query_user_by_username import QueryUserByUserName
from domain.users.adapters import UsersRepository
from domain.users.commands import RegisterUser
from domain.users.events import UserRegistered
from domain.users.exceptions import DuplicatedUserName
from domain.users.user import User
from domain.users.value_objects import UserID


class QueryAllUsers(object):
    @inject
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        return self.user_repository.all()


class QueryUserByID(object):
    @inject
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UserID):
        return self.user_repository.by_id(user_id)


class UserRegistrator(object):
    @inject
    def __init__(self, query_user_by_username: QueryUserByUserName):
        self.query_user_by_username = query_user_by_username

    def execute(self, command: RegisterUser) -> Tuple[User, List[UserRegistered]]:
        if self.query_user_by_username.execute(command.username) is not None:
            raise DuplicatedUserName('A user with %s already exists' % command.username)
        return (User(username=command.username, password=command.password, about=command.about, ID=command.ID), [
            UserRegistered(username=command.username, password=command.password, about=command.about, ID=command.ID)])
