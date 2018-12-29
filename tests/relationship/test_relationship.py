from unittest import TestCase

from domain.relationship.relationship import Relationship
from domain.users.user_id import UserID


class TestRelationship(TestCase):
    def test_should_create_a_relationship(self):
        relationship = Relationship(follower_id=UserID('251c6773-18fb-4e83-b19d-5fe9e14aede8'),
                                    followee_id=UserID('2add0450-dbce-4bea-ae48-051d438f1391'))
        assert '2add0450-dbce-4bea-ae48-051d438f1391' == relationship.followee_id.contents
        assert '251c6773-18fb-4e83-b19d-5fe9e14aede8' == relationship.follower_id.contents
