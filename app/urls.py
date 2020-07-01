from django.urls import include, path

from . import routes


handler404 = 'app.routes.handle404'


urlpatterns = [
    path('', routes.index),
    path('posts/', include('app.posts.urls')),
    path('users/', include('app.users.urls')),
    path('users/<int:user_id>/posts/', routes.user_posts_all),
]
