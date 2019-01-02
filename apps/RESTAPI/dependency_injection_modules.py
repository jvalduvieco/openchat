from injector import Binder, SingletonScope

from domain.login.login_by_username_and_password import UserLoginByUserNameAndPassword
from domain.misc import CommandBus, EventBus
from domain.misc.clock import Clock
from domain.posts.posts_repository import PostsRepository
from domain.posts.query_posts_by_user_id import QueryPostByUserID
from domain.relationship.relationship_repository import RelationshipRepository
from domain.users.query_user_by_id import QueryUserByID
from domain.users.query_user_by_username import QueryUserByUserName
from domain.users.user_registrator import UserRegistrator
from domain.users.users_repository import UsersRepository
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
