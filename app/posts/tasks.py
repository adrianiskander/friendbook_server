def serialize_many_posts(posts):
    return [serialize_post(post) for post in posts]


def serialize_post(post):
    post = {
        'id': post.id,
        'text': post.text,
        'created': post.created,
        'updated': post.updated,
        'isPrivate': post.is_private,
        'isUpdated': post.is_updated,
        'user': {
            'username': post.user.username,
            'firstName': post.user.first_name,
            'lastName': post.user.last_name
        }
    }
    return post
