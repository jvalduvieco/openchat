from posts.post import Post
from posts.post_id import PostID
from tests.fixtures.time import a_perfect_day_and_time, a_perfect_day_and_time_ten_minutes_after
from tests.fixtures.users import maria, bob


def a_post_by_maria():
    return Post(PostID('116c6055-86fe-4335-a332-5a586e995c12'), maria().ID, 'Hi! this is Maria',
                a_perfect_day_and_time())


def a_post_by_bob():
    return Post(PostID('31b7bf07-06ea-45b9-a8ed-f1f0a8d2040b'), bob().ID, 'Hi! this is Bob',
                a_perfect_day_and_time(5))


def another_post_by_maria():
    return Post(PostID('966ff2dd-e839-44c0-adc9-cfc771e3cf13'), maria().ID, 'I\'ve invented something!',
                a_perfect_day_and_time_ten_minutes_after())
