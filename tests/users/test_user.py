from dataclasses import replace
from unittest import TestCase
import uuid

from users.user import User


class TestUser(TestCase):
    def test_should_create_a_user(self):
        user = User(username='Maria', password='uselesspassword', about='About Maria')
        assert user.username == 'Maria'
        assert user.password == 'uselesspassword'
        assert user.about == 'About Maria'

    def test_should_not_allow_username_with_spaces(self):
        with self.assertRaises(ValueError):
            User(username='Maria Lopez', password='uselesspassword', about='About Maria')

    def test_should_create_a_copy_with_new_values(self):
        a_user = User(username='Maria', password='uselesspassword', about='About Maria')
        another_user = replace(a_user, password='thispasswordisuselesstoo')
        assert a_user.username == another_user.username
        assert a_user.about == another_user.about
        assert another_user.password == 'thispasswordisuselesstoo'
        assert a_user != another_user

    def test_two_variables_with_same_values_should_be_equal(self):
        an_id = uuid.uuid4()
        a_user = User(username='Maria', password='uselesspassword', about='About Maria', ID=an_id)
        another_user = User(username='Maria', password='uselesspassword', about='About Maria', ID=an_id)
        assert a_user == another_user
