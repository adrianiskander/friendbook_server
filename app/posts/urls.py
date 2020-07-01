from django.urls import path

from . import routes


urlpatterns = [
    path('', routes.posts_all),
    path('<int:post_id>/', routes.post)
]
