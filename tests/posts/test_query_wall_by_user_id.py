import abc
from dataclasses import dataclass
from typing import List
from unittest import TestCase

from infrastructure.posts.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.users.users_repository_in_memory import InMemoryUsersRepository
from posts.posts_repository import PostsRepository
from tests.fixtures.posts import a_post_by_maria, a_post_by_bob, another_post_by_maria
from tests.fixtures.users import maria, bob_follows_maria, inexistent_user_id
from users.exceptions import UnknownUser
from users.query_user_by_id import QueryUserByID
from users.relationship import Relationship
from users.user_id import UserID


class RelationshipsRepository(abc.ABC):
    @abc.abstractmethod
    def by_followee_id(self, followee_id: UserID) -> List[UserID]:
        pass

    @abc.abstractmethod
    def save(self, relationship: Relationship):
        pass


class InMemoryRelationshipRepository(RelationshipsRepository):
    def __init__(self, initial_relationships=None):
        if initial_relationships is None:
            initial_relationships = []
        self._by_followee_id = {}
        for relationship in initial_relationships:
            self.save(relationship)

    def by_followee_id(self, followee_id: UserID) -> List[UserID]:
        return self._by_followee_id.get(followee_id.contents, [])

    def save(self, relationship: Relationship):
        followers = self._by_followee_id.get(relationship.followee_id.contents, [])
        followers.append(relationship.follower_id)
        self._by_followee_id[relationship.followee_id.contents] = followers


class QueryRelationshipsByFolloweeID(object):
    def __init__(self, relationships_repository: RelationshipsRepository):
        self.relationships_repository = relationships_repository

    def execute(self, user_id: UserID):
        return self.relationships_repository.by_followee_id(user_id)


@dataclass(frozen=True)
class WallByUserID(object):
    user_id: UserID


class QueryWallByUserID(object):
    def __init__(self, query_user_by_id: QueryUserByID,
                 posts_repository: PostsRepository,
                 query_relationships_by_followee_id: QueryRelationshipsByFolloweeID):
        self.query_relationships_by_followee_id = query_relationships_by_followee_id
        self.query_user_by_id = query_user_by_id
        self.posts_repository = posts_repository

    def _posts_by_followers(self, query):
        posts_by_followers = []
        for follower in self.query_relationships_by_followee_id.execute(query.user_id):
            posts_by_followers += self.posts_repository.by_user_id(follower)
        return posts_by_followers

    def execute(self, query: WallByUserID):
        if self.query_user_by_id.execute(query.user_id) is None:
            raise UnknownUser('User %s does not exist' % query.user_id.contents)

        return sorted(self._posts_by_followers(query)
                      + self.posts_repository.by_user_id(query.user_id)
                      , key=lambda x: x.created_at)


class TestCreatePost(TestCase):
    def test_should_get_a_list_of_posts_by_user_id(self):
        query = WallByUserID(user_id=maria().ID)
        posts_by_user_id = QueryWallByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), a_post_by_bob(), another_post_by_maria()]),
            QueryRelationshipsByFolloweeID(InMemoryRelationshipRepository([bob_follows_maria()]))
        )

        post_list = posts_by_user_id.execute(query)

        assert 3 == len(post_list)
        assert a_post_by_maria() in post_list
        assert a_post_by_bob() in post_list
        assert another_post_by_maria() in post_list

    def test_should_throw_an_exception_if_user_does_not_exist(self):
        query = WallByUserID(user_id=inexistent_user_id())
        posts_by_user_id = QueryWallByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), a_post_by_bob(), another_post_by_maria()]),
            QueryRelationshipsByFolloweeID(InMemoryRelationshipRepository([bob_follows_maria()]))
        )
        with self.assertRaises(UnknownUser):
            posts_by_user_id.execute(query)
