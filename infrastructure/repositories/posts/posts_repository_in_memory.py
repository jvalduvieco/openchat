from typing import List

from posts.post import Post
from posts.posts_repository import PostsRepository
from users.user_id import UserID


class InMemoryPostsRepository(PostsRepository):
    def __init__(self, initial_posts=None):
        if initial_posts is None:
            initial_posts = []
        self.posts_by_user_id = {}
        for post in initial_posts:
            self.save(post)

    def by_user_id(self, user_id: UserID) -> List[Post]:
        return self.posts_by_user_id.get(user_id.contents, [])

    def save(self, post: Post) -> None:
        current_posts = self.posts_by_user_id.get(post.user_id.contents, [])
        current_posts.append(post)
        self.posts_by_user_id[post.user_id.contents] = current_posts
