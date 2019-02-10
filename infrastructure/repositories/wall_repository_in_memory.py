from typing import List

from domain.posts.post import Post, post_in
from domain.users.user_id import UserID
from domain.wall.repository import WallRepository


class InMemoryWallRepository(WallRepository):
    def __init__(self, initial_wall_items=None):
        if initial_wall_items is None:
            initial_wall_items = []
        self.wall_by_user_id = {}
        for wall_item in initial_wall_items:
            self.save(wall_item)

    def by_user_id(self, user_id: UserID) -> List[Post]:
        return self.wall_by_user_id.get(user_id.contents.__str__(), None) or []

    def save(self, user_id, event) -> None:
        current_wall = self.wall_by_user_id.get(user_id.contents, [])
        current_wall.append(post_in(event))
        self.wall_by_user_id[user_id.contents.__str__()] = current_wall
