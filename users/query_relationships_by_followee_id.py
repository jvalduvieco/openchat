from users.followers_repository import FollowersRepository
from users.user_id import UserID


class QueryFollowersByFolloweeID(object):
    def __init__(self, followers_repository: FollowersRepository):
        self.followers_repository = followers_repository

    def execute(self, user_id: UserID):
        return self.followers_repository.by_followee_id(user_id)
