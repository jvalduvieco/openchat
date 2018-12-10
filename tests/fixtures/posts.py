from posts.post import Post
from posts.post_id import PostID
from tests.fixtures.time import a_perfect_day_and_time
from tests.fixtures.users import maria


def a_post_by_maria():
    return Post(PostID('116c6055-86fe-4335-a332-5a586e995c12'), maria().ID, 'Hi! this is Maria',
                a_perfect_day_and_time())
