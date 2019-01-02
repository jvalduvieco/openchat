from injector import Injector

from domain.login.login_by_username_and_password import UserLoginByUserNameAndPassword
from domain.login.login_user_command import LoginUser
from domain.misc import CommandBus, EventBus
from domain.posts.create_post_command import CreatePost
from domain.posts.post_creator import PostCreator
from domain.posts.posts_repository import PostsRepository
from domain.relationship.create_relationship import CreateRelationship
from domain.relationship.relationship_creator import RelationshipCreator
from domain.relationship.relationship_repository import RelationshipRepository
from domain.users.register_user_command import RegisterUser
from domain.users.user_registrator import UserRegistrator
from domain.users.users_repository import UsersRepository
from infrastructure.CommandBus.local_command_handler import build_local_command_handler


def user_command_handlers(injector: Injector, command_bus: CommandBus, event_bus: EventBus):
    command_bus.register(**build_local_command_handler(injector, RegisterUser, UserRegistrator, UsersRepository,
                                                       event_bus))
    command_bus.register(**build_local_command_handler(injector, LoginUser, UserLoginByUserNameAndPassword,
                                                       UsersRepository, event_bus))
    command_bus.register(**build_local_command_handler(injector, CreatePost, PostCreator,
                                                       PostsRepository, event_bus))
    command_bus.register(**build_local_command_handler(injector, CreateRelationship, RelationshipCreator,
                                                       RelationshipRepository, event_bus))
