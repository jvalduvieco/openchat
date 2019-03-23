from unittest import TestCase

from parameterized import parameterized

from domain.posts.post import post_in
from domain.wall.repository import WallRepository
from infrastructure.repositories.wall_repository_in_memory import InMemoryWallRepository
from tests.fixtures.posts import maria_created_a_post
from tests.fixtures.users import maria


class TestWallsRepository(TestCase):
    @parameterized.expand([
        [InMemoryWallRepository()]
    ])
    def test_should_save_a_wall_item_and_recover_by_user_id(self, wall_repository: WallRepository):
        a_user = maria()
        event = maria_created_a_post()
        wall_repository.save(a_user.ID, event)

        wall_from_repo = wall_repository.by_user_id(a_user.ID)

        self.assertEqual(1, len(wall_from_repo))
        self.assertEqual(post_in(event), wall_from_repo[0])
