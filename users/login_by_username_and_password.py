from users.exceptions import UnkownUser, InvalidCredentials
from users.login_user_command import LoginUser
from users.query_user_by_username import QueryUserByUserName


class UserLoginByUserNameAndPassword(object):
    def __init__(self, query_user_by_username: QueryUserByUserName):
        self.query_user_by_username = query_user_by_username

    def execute(self, command: LoginUser) -> None:
        user = self.query_user_by_username.execute(command.username)
        if user is None:
            raise UnkownUser('User %s does not exist' % command.username.contents)
        if command.password != user.password:
            raise InvalidCredentials('Credentials for user %s do not match' % command.username.contents)
