from typing import List, Tuple

from users.exceptions import DuplicatedUserName
from users.query_user_by_username import QueryUserByUserName
from users.register_user_command import RegisterUser
from users.user import User
from users.user_registered import UserRegistered


class UserRegistrator(object):
    def __init__(self, query_user_by_username: QueryUserByUserName):
        self.query_user_by_username = query_user_by_username

    def execute(self, command: RegisterUser) -> Tuple[User, List[UserRegistered]]:
        if self.query_user_by_username.execute(command.username) is not None:
            raise DuplicatedUserName('A user with %s already exists' % command.username)
        return (User(username=command.username, password=command.password, about=command.about, ID=command.ID), [
            UserRegistered(username=command.username, password=command.password, about=command.about, ID=command.ID)])
