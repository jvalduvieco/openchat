from typing import List
from typing import Tuple

from injector import inject

from domain.posts.adapters import PostsRepository
from domain.posts.commands import CreatePost
from domain.posts.events import PostCreated
from domain.posts.exceptions import UnkownUserID
from domain.posts.post import Post
from domain.users.exceptions import UnknownUser
from domain.users.services import QueryUserByID


class PostCreator(object):
    @inject
    def __init__(self, query_user_by_id: QueryUserByID):
        self.query_user_by_id = query_user_by_id

    def execute(self, command: CreatePost) -> Tuple[Post, List[PostCreated]]:
        user = self.query_user_by_id.execute(command.user_id)
        if user is None:
            raise UnkownUserID("User %s does not exist" % command.user_id.contents)
        return Post(post_id=command.post_id, user_id=command.user_id, text=command.text,
                    created_at=command.created_at), [
                   PostCreated(post_id=command.post_id, user_id=command.user_id, text=command.text,
                               created_at=command.created_at)]


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
