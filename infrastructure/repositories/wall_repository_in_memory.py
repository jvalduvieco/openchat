from typing import List, Tuple

from domain.posts.post import Post, post_in
from domain.posts.post_created import PostCreated
from domain.users.user_id import UserID
from domain.wall.repository import WallRepository


class InMemoryWallRepository(WallRepository):
    def __init__(self, initial_events: List[Tuple[UserID, List[PostCreated]]] = None):
        if initial_events is None:
            initial_events = []
        self.wall_by_user_id = {}
        for user, events in initial_events:
            [self.save(user, event) for event in events]

    def by_user_id(self, user_id: UserID) -> List[Post]:
        return self.wall_by_user_id.get(user_id.contents.__str__(), None) or []

    def save(self, user_id: UserID, event: PostCreated) -> None:
        key = user_id.contents.__str__()
        current_wall = self.wall_by_user_id.get(key, [])
        current_wall.append(post_in(event))
        self.wall_by_user_id[key] = current_wall
