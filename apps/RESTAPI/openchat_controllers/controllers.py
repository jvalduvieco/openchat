import json
from typing import List

from flask import Blueprint, request

from domain.login.login_user_command import LoginUser
from domain.misc import CommandBus
from domain.users.password import Password
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
