from unittest import TestCase

from domain.users.password import Password


class TestPassword(TestCase):
    def test_should_create_a_password(self):
        a_password = Password('iAmAPassword')

        assert a_password.contents == 'iAmAPassword'

    def test_should_not_allow_password_with_spaces(self):
        with self.assertRaises(ValueError):
            Password('useless password')

    def test_should_not_allow_empty_password(self):
        with self.assertRaises(ValueError):
            Password('')

    def test_should_not_allow_undefined_password(self):
        with self.assertRaises(ValueError):
            Password(None)  # noqa
