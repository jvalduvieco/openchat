import json

from flask import Blueprint, request

from domain.misc import CommandBus
from domain.users.password import Password
from domain.users.register_user_command import RegisterUser
from domain.users.user_id import UserID
from domain.users.user_name import UserName

registration = Blueprint('registration', __name__)


@registration.route('/registration', methods=['POST'])
def registration_post(command_bus: CommandBus):
    client_request = request.json
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
    return json.dumps(response)
