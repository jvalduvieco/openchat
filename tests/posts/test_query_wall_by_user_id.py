from unittest import TestCase

from domain.posts.query_wall_by_user_id import QueryWallByUserID
from domain.posts.wall_by_user_id import WallByUserID
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from infrastructure.repositories.posts.posts_repository_in_memory import InMemoryPostsRepository
from infrastructure.repositories.relationship.relationship_repository_in_memory import InMemoryRelationshipRepository
from infrastructure.repositories.users.users_repository_in_memory import InMemoryUsersRepository
from tests.fixtures.posts import a_post_by_maria, a_post_by_bob, another_post_by_maria
from tests.fixtures.users import maria, bob_follows_maria, inexistent_user_id
from domain.relationship.query_relationships_by_followee_id import QueryFollowersByFolloweeID


class TestCreatePost(TestCase):
    def test_should_get_a_list_of_posts_by_user_id(self):
        query = WallByUserID(user_id=maria().ID)
        posts_by_user_id = QueryWallByUserID(
            QueryUserByID(InMemoryUsersRepository([maria()])),
            InMemoryPostsRepository([a_post_by_maria(), a_post_by_bob(), another_post_by_maria()]),
            QueryFollowersByFolloweeID(InMemoryRelationshipRepository([bob_follows_maria()]))
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
            QueryFollowersByFolloweeID(InMemoryRelationshipRepository([bob_follows_maria()]))
        )

        with self.assertRaises(UnknownUser):
            posts_by_user_id.execute(query)
