from injector import Injector

from domain.login.commands import LoginUser
from domain.login.services import UserLoginByUserNameAndPassword
from domain.misc import CommandBus, EventBus
from domain.posts.adapters import PostsRepository
from domain.posts.commands import CreatePost
from domain.posts.services import PostCreator
from domain.relationship.adapters import RelationshipRepository
from domain.relationship.commands import CreateRelationship
from domain.relationship.services import RelationshipCreator
from domain.users.adapters import UsersRepository
from domain.users.commands import RegisterUser
from domain.users.services import UserRegistrator
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
