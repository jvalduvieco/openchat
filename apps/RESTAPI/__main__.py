import os
from typing import List, Callable

from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import Binder, Injector, SingletonScope

from apps.RESTAPI.error_handler import handle_invalid_usage
from apps.RESTAPI.openchat_controllers.controllers import openchat_controllers
from domain.login.login_by_username_and_password import UserLoginByUserNameAndPassword
from domain.login.login_user_command import LoginUser
from domain.misc import CommandBus, EventBus
from domain.misc.clock import Clock
from domain.posts.create_post_command import CreatePost
from domain.posts.post_creator import PostCreator
from domain.posts.posts_repository import PostsRepository
from domain.posts.query_posts_by_user_id import QueryPostByUserID
from domain.relationship.relationship_repository import RelationshipRepository
from domain.users.query_user_by_id import QueryUserByID
from domain.users.query_user_by_username import QueryUserByUserName
from domain.users.register_user_command import RegisterUser
from domain.users.user_registrator import UserRegistrator
from domain.users.users_repository import UsersRepository
from infrastructure.CommandBus.local_command_handler import build_local_command_handler
from infrastructure.CommandBus.local_synchronous_command_bus import LocalSynchronousCommandBus
from infrastructure.clock.real_clock import RealClock
from infrastructure.local_synchronous_event_bus import LocalSynchronousEventBus
from infrastructure.repositories.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.repositories.relationship_repository_in_memory import InMemoryRelationshipRepository
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository


def user(binder: Binder):
    binder.bind(UsersRepository, InMemoryUsersRepository(), scope=SingletonScope)
    binder.bind(PostsRepository, InMemoryPostsRepository(), scope=SingletonScope)
    binder.bind(RelationshipRepository, InMemoryRelationshipRepository(), scope=SingletonScope)
    binder.bind(Clock, RealClock(), scope=SingletonScope)
    binder.bind(QueryUserByUserName)
    binder.bind(QueryUserByID)
    binder.bind(QueryPostByUserID)
    binder.bind(UserRegistrator)
    binder.bind(UserLoginByUserNameAndPassword)


def core(binder: Binder):
    binder.bind(CommandBus, to=lambda: LocalSynchronousCommandBus(), scope=SingletonScope)
    binder.bind(EventBus, to=lambda: LocalSynchronousEventBus(), scope=SingletonScope)


def user_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus):
    command_bus.register(RegisterUser,
                         build_local_command_handler(injector, RegisterUser, UserRegistrator, UsersRepository,
                                                     event_bus))
    command_bus.register(LoginUser,
                         build_local_command_handler(injector, LoginUser, UserLoginByUserNameAndPassword,
                                                     UsersRepository, event_bus))
    command_bus.register(CreatePost,
                         build_local_command_handler(injector, CreatePost, PostCreator,
                                                     PostsRepository, event_bus))


def register_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus,
                              modules: List[Callable]):
    for module in modules:
        module(injector, command_bus, event_bus)


def create_openchat_app(config=None, environment=None):
    openchat = Flask(__name__)
    openchat.config.update(config or {})
    openchat.config['ENV'] = environment
    openchat.config['TESTING'] = True if environment != 'production' else False
    openchat.config['DEBUG'] = True if environment != 'production' else False
    CORS(openchat, resources={r"/*": {"origins": "*"}})
    openchat.register_blueprint(openchat_controllers)
    injector = Injector()
    FlaskInjector(app=openchat, injector=injector, modules=[core, user])
    register_command_handlers(injector, injector.get(CommandBus), injector.get(EventBus),
                              modules=[user_command_handlers])
    openchat.register_error_handler(ValueError, handle_invalid_usage)
    return openchat


if __name__ == "__main__":
    config = {
        'SERVER_NAME': "%s:%s" % (os.environ.get('LISTEN', 'localhost'), os.environ.get('PORT', 8080)),
    }
    app = create_openchat_app(config=config, environment=os.environ.get('ENV', 'development'))
    app.run()
