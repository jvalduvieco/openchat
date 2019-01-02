from typing import List, Callable

from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder, Injector, SingletonScope

from apps.RESTAPI.controllers.registration import registration
from domain.misc import CommandBus, EventBus
from domain.posts.posts_repository import PostsRepository
from domain.relationship.relationship_repository import RelationshipRepository
from domain.users.query_user_by_username import QueryUserByUserName
from domain.users.register_user_command import RegisterUser
from domain.users.user_registrator import UserRegistrator
from domain.users.users_repository import UsersRepository
from infrastructure.CommandBus.local_command_handler import build_local_command_handler
from infrastructure.CommandBus.local_synchronous_command_bus import LocalSynchronousCommandBus
from infrastructure.local_synchronous_event_bus import LocalSynchronousEventBus
from infrastructure.repositories.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.repositories.relationship_repository_in_memory import InMemoryRelationshipRepository
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository


def user(binder: Binder):
    binder.bind(UsersRepository, to=lambda: InMemoryUsersRepository(), scope=SingletonScope)
    binder.bind(PostsRepository, to=lambda: InMemoryPostsRepository(), scope=SingletonScope)
    binder.bind(RelationshipRepository, to=lambda: InMemoryRelationshipRepository(), scope=SingletonScope)
    binder.bind(QueryUserByUserName, scope=SingletonScope)
    binder.bind(UserRegistrator)


def core(binder: Binder):
    binder.bind(CommandBus, to=lambda: LocalSynchronousCommandBus(), scope=SingletonScope)
    binder.bind(EventBus, to=lambda: LocalSynchronousEventBus(), scope=SingletonScope)


def user_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus):
    command_bus.register(RegisterUser,
                         build_local_command_handler(injector, RegisterUser, UserRegistrator, InMemoryUsersRepository,
                                                     event_bus))


def register_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus,
                              modules: List[Callable]):
    for module in modules:
        module(injector, command_bus, event_bus)


def create_app():
    an_app = Flask(__name__)

    an_app.register_blueprint(registration)
    injector = Injector()
    FlaskInjector(app=an_app, injector=injector, modules=[core, user])
    register_command_handlers(injector, injector.get(CommandBus), injector.get(EventBus),
                              modules=[user_command_handlers])
    return an_app


if __name__ == "__main__":
    app = create_app()
    app.run()
