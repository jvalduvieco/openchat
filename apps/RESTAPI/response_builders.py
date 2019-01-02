from collections import Iterable


def to_single_user_response(user):
    return {'username': user.username.contents, 'about': user.about, 'id': user.ID.contents.__str__()}


def to_multiple_user_response(users):
    assert isinstance(users, Iterable)
    return [to_single_user_response(user) for user in users]


def to_single_post_response(post):
    return {"postId": post.post_id.contents.__str__(), "userId": post.user_id.contents.__str__(), "text": post.text,
            "dateTime": post.created_at.__str__()}


def to_multiple_post_response(posts):
    assert isinstance(posts, Iterable)
    return [to_single_post_response(post) for post in posts]
