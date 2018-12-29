from domain.relationship.relationship import Relationship
from domain.users.password import Password
from domain.users.register_user_command import RegisterUser
from domain.users.user import User
from domain.users.user_id import UserID
from domain.users.user_name import UserName


def maria() -> User:
    return User(username=UserName('Maria'),
                password=Password('a_password'),
                about='About Maria',
                ID=UserID('331bfef4-7fe9-47b6-a138-42e81d4a5e14'))


def bob() -> User:
    return User(username=UserName('Bob'),
                password=Password('another_password'),
                about='About Bob',
                ID=UserID('0d43fe15-8ffa-4845-a818-ddba840501b2'))


def create_maria() -> RegisterUser:
    return RegisterUser(ID=UserID(),
                        username=UserName('Maria'),
                        password=Password('a_password'),
                        about='About Maria')


def bob_follows_maria():
    return Relationship(follower_id=bob().ID,
                        followee_id=maria().ID)


def inexistent_user_id():
    return UserID('29a9fe4a-b9f9-4326-8937-8df3d41687c4')
