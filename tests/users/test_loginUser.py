from unittest import TestCase

from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.user import maria
from users.login_by_username_and_password import UserLoginByUserNameAndPassword
from users.exceptions import UnkownUser, InvalidCredentials
from users.login_user_command import LoginUser
from users.password import Password
from users.query_user_by_username import QueryUserByUserName
from users.user_name import UserName


class TestLoginUser(TestCase):
    def test_should_login_a_user(self):
        try:
            command = LoginUser(username=UserName('Maria'), password=Password('a_password'))
            user_login_by_username_and_password = UserLoginByUserNameAndPassword(
                QueryUserByUserName(InMemoryUsersRepository([maria()])))
            user_login_by_username_and_password.execute(command)
        except ValueError as err:
            self.fail("Unexpected exception raised: %s" % err)

    def test_should_raise_an_exception_on_unkown_username(self):
            command = LoginUser(username=UserName('IDontExist'), password=Password('a_password'))
            user_login_by_username_and_password = UserLoginByUserNameAndPassword(
                QueryUserByUserName(InMemoryUsersRepository([maria()])))
            with self.assertRaises(UnkownUser):
                user_login_by_username_and_password.execute(command)

    def test_should_raise_an_exception_on_wrong_password(self):
            command = LoginUser(username=UserName('Maria'), password=Password('a_wrong_password'))
            user_login_by_username_and_password = UserLoginByUserNameAndPassword(
                QueryUserByUserName(InMemoryUsersRepository([maria()])))
            with self.assertRaises(InvalidCredentials):
                user_login_by_username_and_password.execute(command)
