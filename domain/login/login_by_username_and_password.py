from typing import Tuple, List
from domain.login.login_user_command import LoginUser
from domain.misc.clock import Clock
from domain.users.exceptions import UnknownUser, InvalidCredentials
from domain.users.query_user_by_username import QueryUserByUserName
from domain.login.user_signed_in import UserSignedIn


class UserLoginByUserNameAndPassword(object):
    def __init__(self, query_user_by_username: QueryUserByUserName, clock: Clock):
        self.clock = clock
        self.query_user_by_username = query_user_by_username

    def execute(self, command: LoginUser) -> Tuple[None, List[UserSignedIn]]:
        user = self.query_user_by_username.execute(command.username)
        if user is None:
            raise UnknownUser('User %s does not exist' % command.username.contents)
        if command.password != user.password:
            raise InvalidCredentials('Credentials for user %s do not match' % command.username.contents)
        return None, [UserSignedIn(username=command.username, timestamp=self.clock.now())]
