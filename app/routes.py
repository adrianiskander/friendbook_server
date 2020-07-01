from django.conf import settings
from django.shortcuts import redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.posts.models import Post
from app.posts.tasks import serialize_many_posts


def handle404(request, exception):
    return redirect(settings.CLIENT_URL)


def index(request):
    return redirect(settings.CLIENT_URL)


@api_view(['GET'])
@permission_classes([AllowAny])
def user_posts_all(request, user_id):

    posts = []

    if request.auth:
        posts = request.user.post_set.all()
    else:
        posts = Post.objects\
            .filter(user_id=user_id)\
            .filter(is_private=False)\
            .all()

    return Response(serialize_many_posts(posts), status=200)
