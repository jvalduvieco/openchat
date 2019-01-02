from typing import List

from injector import inject

from domain.posts.post import Post
from domain.posts.posts_repository import PostsRepository
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID


class QueryPostByUserID(object):
    @inject
    def __init__(self, query_users_by_id: QueryUserByID, posts_repository: PostsRepository):
        self.query_users_by_id = query_users_by_id
        self.posts_repository = posts_repository

    def execute(self, query) -> List[Post]:
        user = self.query_users_by_id.execute(query.user_id)
        if user is None:
            raise UnknownUser('User %s does not exist' % query.user_id.contents)
        return self.posts_repository.by_user_id(query.user_id)
