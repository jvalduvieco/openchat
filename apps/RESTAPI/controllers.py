from flask import Blueprint, request

from apps.RESTAPI.response_builders import to_multiple_user_response, to_multiple_post_response, \
    to_single_user_response, \
    to_single_post_response
from apps.RESTAPI.tools import validate_client_request, return_json
from domain.login.commands import LoginUser
from domain.misc import CommandBus
from domain.misc.clock import Clock
from domain.posts.commands import CreatePost
from domain.posts.queries import PostsByUserID
from domain.posts.services import QueryPostByUserID
from domain.posts.value_objects import PostID
from domain.relationship.commands import CreateRelationship
from domain.relationship.services import QueryRelationshipsByFollowerID
from domain.services.query_user_by_username import QueryUserByUserName
from domain.users.commands import RegisterUser
from domain.users.services import QueryAllUsers, QueryUserByID
from domain.users.value_objects import Password, UserID, UserName
from domain.wall.queries import WallByUserID
from domain.wall.services import QueryWallByUserID

openchat_controllers = Blueprint('openchat_controllers', __name__)


@openchat_controllers.route('/login', methods=['POST'])
@return_json
def login_post(command_bus: CommandBus, query: QueryUserByUserName):
    client_request = request.json
    validate_client_request(client_request, ['username', 'password'])
    login_a_user_command = LoginUser(
        username=UserName(client_request['username']),
        password=Password(client_request['password']),
    )
    command_bus.handle(login_a_user_command)
    user = query.execute(UserName(client_request['username']))

    return to_single_user_response(user), 200


@openchat_controllers.route('/users', methods=['POST'])
@return_json
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

    return to_single_user_response(register_a_user_command), 201


@openchat_controllers.route('/users/<user_id>', methods=['GET'])
@return_json
def get_user_by_id(user_id, query: QueryUserByID):
    return to_multiple_user_response([query.execute(UserID(user_id))]), 200


@openchat_controllers.route('/users', methods=['GET'])
@return_json
def get_all_users(query: QueryAllUsers):
    return to_multiple_user_response(query.execute()), 200


@openchat_controllers.route('/users/<user_id>/timeline', methods=['POST'])
@return_json
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

    return to_single_post_response(create_post_command), 201


@openchat_controllers.route('/users/<user_id>/timeline', methods=['GET'])
@return_json
def get_user_timeline(query: QueryPostByUserID, user_id):
    return to_multiple_post_response(query.execute(PostsByUserID(UserID(user_id)))), 200


@openchat_controllers.route('/users/<user_id>/wall', methods=['GET'])
@return_json
def get_user_wall(query: QueryWallByUserID, user_id):
    posts = query.execute(WallByUserID(UserID(user_id)))
    return to_multiple_post_response(posts), 200


@openchat_controllers.route('/followings', methods=['POST'])
@return_json
def followings_post(command_bus: CommandBus):
    client_request = request.json
    validate_client_request(client_request, ['followerId', 'followeeId'])
    create_relationship_command = CreateRelationship(
        follower_id=UserID(client_request['followerId']),
        followee_id=UserID(client_request['followeeId']),
    )
    command_bus.handle(create_relationship_command)

    return "", 201


@openchat_controllers.route('/followings/<user_id>/followees', methods=['GET'])
@return_json
def get_user_followers(relationships_query: QueryRelationshipsByFollowerID, users_query: QueryUserByID, user_id):
    relationships = relationships_query.execute(UserID(user_id))

    followees_with_data = [users_query.execute(relationship.followee_id) for relationship in relationships]
    return to_multiple_user_response(followees_with_data), 200
