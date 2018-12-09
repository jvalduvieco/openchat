from posts.create_post_command import CreatePost
from users.query_user_by_id import QueryUserByID
from posts.post import Post


class PostCreator(object):
    def __init__(self, query_user_by_id: QueryUserByID):
        self.query_user_by_id = query_user_by_id

    def execute(self, command: CreatePost):
        user = self.query_user_by_id.execute(command.user_id)
        if user is not None:
            return Post(post_id=command.post_id,
                        user_id=command.user_id,
                        text=command.text,
                        created_at=command.created_at)
