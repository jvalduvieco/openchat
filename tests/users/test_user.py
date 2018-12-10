from dataclasses import replace
from unittest import TestCase

from users.password import Password
from users.user import User
from users.user_id import UserID
from users.user_name import UserName


class TestUser(TestCase):
    def test_should_create_a_user(self):
        user = User(username=UserName('Maria'), password=Password('uselesspassword'), about='About Maria')
        assert user.username.contents == 'Maria'
        assert user.password.contents == 'uselesspassword'
        assert user.about == 'About Maria'

    def test_should_create_a_copy_with_new_values(self):
        a_user = User(username=UserName('Maria'), password=Password('uselesspassword'), about='About Maria')
        user_with_password_changed = replace(a_user, password=Password('thispasswordisuselesstoo'))
        assert a_user.username == user_with_password_changed.username
        assert a_user.about == user_with_password_changed.about
        assert user_with_password_changed.password.contents == 'thispasswordisuselesstoo'
        assert a_user != user_with_password_changed

    def test_two_variables_with_same_values_should_be_equal(self):
        an_id = UserID()
        a_user = User(
            username=UserName('Maria'),
            password=Password('uselesspassword'),
            about='About Maria',
            ID=an_id)
        another_user = User(
            username=UserName('Maria'),
            password=Password('uselesspassword'),
            about='About Maria',
            ID=an_id)
        assert a_user == another_user
