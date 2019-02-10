from injector import inject

from domain.users.exceptions import UnknownUser
from domain.users.query_user_by_id import QueryUserByID
from domain.wall.by_user_id import WallByUserID
from domain.wall.repository import WallRepository


class QueryWallByUserID(object):
    @inject
    def __init__(self, query_user_by_id: QueryUserByID,
                 wall_repository: WallRepository):
        self.query_user_by_id = query_user_by_id
        self.wall_repository = wall_repository

    def execute(self, query: WallByUserID):
        if self.query_user_by_id.execute(query.user_id) is None:
            raise UnknownUser('User %s does not exist' % query.user_id.contents)

        return self.wall_repository.by_user_id(query.user_id)
