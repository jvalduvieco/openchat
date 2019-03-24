from injector import Binder, SingletonScope

from domain.login.services import UserLoginByUserNameAndPassword
from domain.misc import CommandBus, EventBus
from domain.misc.clock import Clock
from domain.posts.adapters import PostsRepository
from domain.posts.services import QueryPostByUserID
from domain.relationship.adapters import RelationshipRepository
from domain.services.query_user_by_username import QueryUserByUserName
from domain.users.adapters import UsersRepository
from domain.users.services import QueryUserByID, UserRegistrator
from domain.wall.adapters import WallRepository
from infrastructure.CommandBus.local_synchronous_command_bus import LocalSynchronousCommandBus
from infrastructure.EventBus.local_synchronous_event_bus import LocalSynchronousEventBus
from infrastructure.clock.real_clock import RealClock
from infrastructure.repositories.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.repositories.relationship_repository_in_memory import InMemoryRelationshipRepository
from infrastructure.repositories.users_repository_in_memory import InMemoryUsersRepository
from infrastructure.repositories.wall_repository_in_memory import InMemoryWallRepository


def user(binder: Binder):
    binder.bind(UsersRepository, InMemoryUsersRepository(), scope=SingletonScope)
    binder.bind(PostsRepository, InMemoryPostsRepository(), scope=SingletonScope)
    binder.bind(RelationshipRepository, InMemoryRelationshipRepository(), scope=SingletonScope)
    binder.bind(WallRepository, InMemoryWallRepository(), scope=SingletonScope)
    binder.bind(Clock, RealClock(), scope=SingletonScope)
    binder.bind(QueryUserByUserName)
    binder.bind(QueryUserByID)
    binder.bind(QueryPostByUserID)
    binder.bind(UserRegistrator)
    binder.bind(UserLoginByUserNameAndPassword)


def core(binder: Binder):
    binder.bind(CommandBus, to=lambda: LocalSynchronousCommandBus(), scope=SingletonScope)
    binder.bind(EventBus, to=lambda: LocalSynchronousEventBus(), scope=SingletonScope)
