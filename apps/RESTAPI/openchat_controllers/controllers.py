import json
from typing import List

from flask import Blueprint, request

from domain.login.login_user_command import LoginUser
from domain.misc import CommandBus
from domain.misc.clock import Clock
from domain.posts.create_post_command import CreatePost
from domain.posts.post_id import PostID
from domain.posts.posts_by_user_id_query import PostsByUserID
from domain.posts.query_posts_by_user_id import QueryPostByUserID
from domain.relationship.create_relationship import CreateRelationship
from domain.users.password import Password
from domain.users.query_all_users import QueryAllUsers
from domain.users.query_user_by_id import QueryUserByID
from domain.users.query_user_by_username import QueryUserByUserName
from domain.users.register_user_command import RegisterUser
from domain.users.user_id import UserID
from domain.users.user_name import UserName

openchat_controllers = Blueprint('openchat_controllers', __name__)


def find_missing_keys(keys, expected_keys):
    return [key for key in expected_keys if key not in keys]


def validate_client_request(client_request: dict, expected_keys: List[str]):
    if type(client_request) is not dict:
        raise ValueError("Invalid request")
    missing_keys = find_missing_keys(client_request, expected_keys)
    if len(missing_keys) > 0:
        raise ValueError("Invalid request: Missing keys (%s)" % missing_keys)


@openchat_controllers.route('/login', methods=['POST'])
def login_post(command_bus: CommandBus, query: QueryUserByUserName):
    client_request = request.json
    validate_client_request(client_request, ['username', 'password'])
    login_a_user_command = LoginUser(
        username=UserName(client_request['username']),
        password=Password(client_request['password']),
    )
    command_bus.handle(login_a_user_command)
    user = query.execute(UserName(client_request['username']))

    response = {
        'username': login_a_user_command.username.contents,
        'password': login_a_user_command.password.contents,
        'about': user.about,
        'id': user.ID.contents.__str__()
    }
    return json.dumps(response), 200


@openchat_controllers.route('/users', methods=['POST'])
def registration_post(command_bus: CommandBus):
    client_request = request.json
    validate_client_request(client_request, ['username', 'password', 'about'])
    register_a_user_command = RegisterUser(
        username=UserName(client_request['username']),
        password=Password(client_request['password']),
        about=client_request['about'],
        ID=UserID()
    )
    command_bus.handle(register_a_user_command)

    response = {
        'username': register_a_user_command.username.contents,
        'password': register_a_user_command.password.contents,
        'about': register_a_user_command.about,
        'id': register_a_user_command.ID.contents.__str__()
    }
    return json.dumps(response), 201


@openchat_controllers.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id, query: QueryUserByID):
    user = query.execute(UserID(user_id))
    return json.dumps({'username': user.username.contents, 'about': user.about, 'id': user.ID.contents.__str__()}), 200


@openchat_controllers.route('/users', methods=['GET'])
def get_all_users(query: QueryAllUsers):
    users = [
        {'username': user.username.contents, 'about': user.about, 'id': user.ID.contents.__str__()}
        for user in query.execute()]
    return json.dumps(users), 200


@openchat_controllers.route('/users/<user_id>/timeline', methods=['POST'])
def create_post(command_bus: CommandBus, clock: Clock, user_id):
    client_request = request.json
    validate_client_request(client_request, ['text'])
    create_post_command = CreatePost(
        post_id=PostID(),
        user_id=UserID(user_id),
        text=client_request['text'],
        created_at=clock.now()
    )
    command_bus.handle(create_post_command)

    response = {
        'userId': create_post_command.user_id.contents.__str__(),
        'text': create_post_command.text,
        'postId': create_post_command.post_id.contents.__str__(),
        'dateTime': create_post_command.created_at.__str__()
    }
    return json.dumps(response), 201


@openchat_controllers.route('/users/<user_id>/timeline', methods=['GET'])
def get_user_timeline(query: QueryPostByUserID, user_id):
    posts = query.execute(PostsByUserID(UserID(user_id)))

    response = [
        {"postId": post.post_id.contents.__str__(), "userId": post.user_id.contents.__str__(), "text": post.text,
         "dateTime": post.created_at.__str__()} for post in
        posts]
    return json.dumps(response), 200


@openchat_controllers.route('/followings', methods=['POST'])
def followings_post(command_bus: CommandBus):
    client_request = request.json
    validate_client_request(client_request, ['followerId', 'followeeId'])
    create_relationship_command = CreateRelationship(
        follower_id=UserID(client_request['followerId']),
        followee_id=UserID(client_request['followeeId']),
    )
    command_bus.handle(create_relationship_command)

    return "", 201
