from domain.posts.posts_repository import PostsRepository
from domain.posts.wall_by_user_id import WallByUserID
from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from domain.relationship.query_relationships_by_followee_id import QueryFollowersByFolloweeID


class QueryWallByUserID(object):
    def __init__(self, query_user_by_id: QueryUserByID,
                 posts_repository: PostsRepository,
                 query_relationships_by_followee_id: QueryFollowersByFolloweeID):
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
                      + self.posts_repository.by_user_id(query.user_id), key=lambda x: x.created_at)
