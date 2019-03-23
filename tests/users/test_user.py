from dataclasses import replace
from unittest import TestCase

from domain.users.password import Password
from domain.users.user import User
from domain.users.user_id import UserID
from domain.users.user_name import UserName


class TestUser(TestCase):
    def test_should_create_a_user(self):
        user = User(username=UserName('Maria'), password=Password('uselesspassword'), about='About Maria')

        self.assertEqual('Maria', user.username.contents)
        self.assertEqual('uselesspassword', user.password.contents)
        self.assertEqual('About Maria', user.about)

    def test_should_create_a_copy_with_new_values(self):
        a_user = User(username=UserName('Maria'), password=Password('uselesspassword'), about='About Maria')

        user_with_password_changed = replace(a_user, password=Password('thispasswordisuselesstoo'))

        self.assertEqual(a_user.username, user_with_password_changed.username)
        self.assertEqual(a_user.about, user_with_password_changed.about)
        self.assertEqual('thispasswordisuselesstoo', user_with_password_changed.password.contents)
        self.assertNotEqual(a_user, user_with_password_changed)

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

        self.assertEqual(a_user, another_user)
