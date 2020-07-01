from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import tasks
from .forms import PostForm
from .models import Post


@api_view(['DELETE', 'PUT'])
def post(request, post_id):
    """
        Specific post route.
    """
    post = request.user.post_set.filter(id=post_id).first()

    if not post:
        return Response(status=404)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=204)

    elif request.method == 'PUT':

        form = PostForm(request.data)

        if not form.is_valid():
            return Response(status=400)

        post.text = form.cleaned_data.get('text')
        post.is_private = form.cleaned_data.get('isPrivate')
        post.is_updated = True
        post.save()
        return Response(tasks.serialize_post(post), status=200)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def posts_all(request):

    form = None
    posts = []

    if request.method == 'POST':

        if not request.auth:
            return Response(status=401)

        form = PostForm(request.data)

        if form.is_valid():
            post = Post.objects.create(
                text=form.cleaned_data.get('text'),
                is_private=form.cleaned_data.get('isPrivate'),
                user=request.user
            )
            return Response(tasks.serialize_post(post), status=201)
        return Response(status=400)

    posts = Post.objects.filter(is_private=False).all()

    return Response(tasks.serialize_many_posts(posts), status=200)
