from unittest import TestCase

from infrastructure.clock.fake_clock import FakeClock
from infrastructure.repositories.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.users import maria
from users.login_by_username_and_password import UserLoginByUserNameAndPassword
from users.exceptions import UnknownUser, InvalidCredentials
from users.login_user_command import LoginUser
from users.password import Password
from users.query_user_by_username import QueryUserByUserName
from users.user_name import UserName


class TestLoginUser(TestCase):
    def test_should_login_a_user(self):
        try:
            command = LoginUser(username=UserName('Maria'), password=Password('a_password'))
            user_login_by_username_and_password = UserLoginByUserNameAndPassword(
                QueryUserByUserName(InMemoryUsersRepository([maria()])), FakeClock(a_perfect_day_and_time()))

            entity, events = user_login_by_username_and_password.execute(command)

            assert entity is None
            assert len(events) == 1
            assert events[0].username == command.username
            assert events[0].timestamp == a_perfect_day_and_time()

        except ValueError as err:
            self.fail("Unexpected exception raised: %s" % err)

    def test_should_raise_an_exception_on_unkown_username(self):
        command = LoginUser(username=UserName('IDontExist'), password=Password('a_password'))

        user_login_by_username_and_password = UserLoginByUserNameAndPassword(
            QueryUserByUserName(InMemoryUsersRepository([maria()])), FakeClock(a_perfect_day_and_time()))

        with self.assertRaises(UnknownUser):
            user_login_by_username_and_password.execute(command)

    def test_should_raise_an_exception_on_wrong_password(self):
        command = LoginUser(username=UserName('Maria'), password=Password('a_wrong_password'))

        user_login_by_username_and_password = UserLoginByUserNameAndPassword(
            QueryUserByUserName(InMemoryUsersRepository([maria()])), FakeClock(a_perfect_day_and_time()))

        with self.assertRaises(InvalidCredentials):
            user_login_by_username_and_password.execute(command)
