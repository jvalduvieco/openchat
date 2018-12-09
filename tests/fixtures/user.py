from uuid import uuid4

from users.password import Password
from users.register_user_command import RegisterUser
from users.user import User
from users.user_id import UserID
from users.user_name import UserName


def maria() -> User:
    return User(username=UserName('Maria'),
                password=Password('a_password'),
                about='About Maria',
                ID=UserID('331bfef4-7fe9-47b6-a138-42e81d4a5e14'))


def create_maria() -> RegisterUser:
    return RegisterUser(ID=UserID(),
                        username=UserName('Maria'),
                        password=Password('a_password'),
                        about='About Maria')
