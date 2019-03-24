from injector import inject

from domain.users.exceptions import UnknownUser
from domain.users.services import QueryUserByID
from domain.wall.adapters import WallRepository
from domain.wall.queries import WallByUserID


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
