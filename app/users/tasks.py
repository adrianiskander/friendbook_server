import time

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import signing
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token as AuthToken

from .forms import AuthForm
from .models import Account


def authenticate_user(**kwargs):
    """
        Authenticate user by email and password.
    """
    user = User.objects.filter(email=kwargs.get('email')).first()
    if not user:
        return None

    user = authenticate(
        username=user.username,
        password=kwargs.get('password')
    )
    if not user:
        return None

    return user


def create_user(request):
    """
        Create user if data is valid and email unique.
    """
    form = AuthForm(request.data)
    if not form.is_valid():
        return None

    if User.objects.filter(email=form.cleaned_data.get('email')).first():
        return None

    user = User.objects.create_user(
        email=form.cleaned_data.get('email'),
        password=form.cleaned_data.get('password'),
        username=f'u{ str(int(time.time())) }',
        is_active=False
    )
    Account.objects.create(user=user)
    AuthToken.objects.create(user=user)

    data = {
        'user': user,
        'request': request
    }
    send_user_activation_token(**data)

    return user


def send_user_activation_token(**kwargs):

    request = kwargs.get('request')
    token = {
        'action': 'activateAccount',
        'userId': kwargs.get('user').id
    }
    token = signing.dumps(token)
    url = request.build_absolute_uri(f'/users/tokens/handle/{token}/')
    msg = f'To activate your account, click the following link:\n\n{url}'

    kwargs.get('user').account.token = token
    kwargs.get('user').account.save()

    send_mail(
        'Activate Account',
        msg,
        settings.EMAIL_HOST_USER,
        [kwargs.get('user').email],
        fail_silently=False,
    )

    if settings.DEBUG:
        print(f'\n{msg}\n')


def send_user_delete_token(request):

    user = User.objects.filter(id=request.user.id).first()
    if not user:
        return None

    token = {
        'action': 'DELETE',
        'userId': user.id
    }

    token = signing.dumps(token)
    url = request.build_absolute_uri(f'/users/tokens/handle/{token}/')
    msg = f'To delete your account, click the following link:\n\n{url}'

    user.account.token = token
    user.account.save()

    send_mail(
        'Delete Account',
        msg,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False,
    )

    if settings.DEBUG:
        print(f'\n{msg}\n')


def send_user_email_change_token(**kwargs):

    # Ensure new email is not already taken by other user.
    if User.objects.filter(email=kwargs.get('email')).first():
        return None

    token = {
        'action': 'updateEmail',
        'email': kwargs.get('email'),
        'userId': kwargs.get('request').user.id
    }
    token = signing.dumps(token)
    url = kwargs.get('request').build_absolute_uri(f'/users/tokens/handle/{token}/')
    msg = f'To confirm this email, click the following link:\n\n{url}'

    kwargs.get('request').user.account.token = token
    kwargs.get('request').user.account.save()

    send_mail(
        'Confirm email',
        msg,
        settings.EMAIL_HOST_USER,
        [kwargs.get('email')],
        fail_silently=False,
    )

    if settings.DEBUG:
        print(f'\n{msg}\n')


def send_user_email_reset_token(**kwargs):

    user = User.objects.filter(email=kwargs.get("email")).first()
    if not user:
        return None

    token = {
        'action': 'resetPassword',
        'userId': user.id,
    }
    token = signing.dumps(token)
    url = kwargs.get("request").build_absolute_uri(f'/users/tokens/handle/{token}/')
    msg = f'To reset your password, click the following link:\n\n{url}'

    user.account.token = token
    user.account.save()

    send_mail(
        'Reset Password',
        msg,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    if settings.DEBUG:
        print(f'\n{msg}\n')


def serialize_user(user):
    data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'token': AuthToken.objects.get(user=user).key
    }
    return data


def serialize_public_user(user):
    data = {
        'id': user.id,
        'username': user.username
    }
    return data
