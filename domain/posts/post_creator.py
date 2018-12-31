from typing import Tuple
from typing import List

from domain.posts.create_post_command import CreatePost
from domain.posts.exceptions import UnkownUserID
from domain.posts.post import Post
from domain.posts.post_created import PostCreated
from domain.users.query_user_by_id import QueryUserByID


class PostCreator(object):
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
