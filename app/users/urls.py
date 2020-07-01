from django.urls import path

from . import routes


urlpatterns = [
    path('', routes.users_all),
    path('email/reset/', routes.user_email_reset),
    path('login/', routes.user_login),
    path('logout/', routes.user_logout),
    path('<username>/', routes.user),
    path('tokens/confirm/<token>/', routes.account_token_confirm),
    path('tokens/handle/<token>/', routes.account_token_handle),
]
