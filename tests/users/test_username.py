from unittest import TestCase

from users.user_name import UserName


class TestUserName(TestCase):
    def test_should_create_a_username(self):

        a_username = UserName('maria')

        assert a_username.contents == 'maria'

    def test_should_not_allow_username_with_spaces(self):
        with self.assertRaises(ValueError):
            UserName('invalid username')
