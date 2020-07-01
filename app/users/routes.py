from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core import signing
from django.db.utils import IntegrityError
from django.shortcuts import redirect

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import forms, tasks


@api_view(['DELETE', 'GET', 'PUT'])
@permission_classes([AllowAny])
def user(request, username):

    if request.method == 'DELETE' and request.auth:
        tasks.send_user_delete_token(request)
        request.user.auth_token.delete()
        return Response('Check your email for confirmation link', status=202)

    elif request.method == 'PUT' and request.auth:

        form = forms.UserUpdateForm(request.data)
        msg = None

        if not form.is_valid():
            msg = 'Submitted data is invalid.'
            return Response({'message': msg}, status=400)

        try:
            request.user.first_name = form.cleaned_data.get('firstName')
            request.user.last_name = form.cleaned_data.get('lastName')
            request.user.username = form.cleaned_data.get('username')
            request.user.save()
        except IntegrityError:
            msg = 'Submitted data is not unique.'
            return Response({'message': msg}, status=400)

        # Client requested email change so send email change confirm token.
        if request.user.email != form.cleaned_data.get('email'):
            data = {
                'email': form.cleaned_data.get('email'),
                'request': request
            }
            tasks.send_user_email_change_token(**data)
            msg = 'Check your new email for confirmation link.'
            return Response({'message': msg}, status=202)

        return Response({'message': msg}, status=204)

    user = User.objects.filter(username=username).first()
    if not user:
        return Response("User doesn't exist.", status=404)

    if not request.auth:
        return Response(tasks.serialize_public_user(user), status=200)

    return Response(tasks.serialize_user(user), status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def users_all(request):

    user = tasks.create_user(request)

    if not user:
        msg = 'Submitted data is invalid or user already exists.'
        return Response({'message': msg}, status=400)

    msg = 'Check your email for account activation link.'
    return Response({'message': msg}, status=202)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_email_reset(request):
    """
        Create and send user email reset token.
    """
    form = forms.EmailForm(request.data)

    if form.is_valid():
        data = {
            'email': form.cleaned_data.get('email'),
            'request': request
        }
        tasks.send_user_email_reset_token(**data)
        return Response('Token sent to given email.', status=202)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
        Login user and create new token.
    """
    user = tasks.authenticate_user(**request.data)

    if not user or not user.is_active:
        return Response(status=400)

    if not Token.objects.filter(user=user).first():
        Token.objects.create(user=user)

    login(request, user)

    return Response(tasks.serialize_user(request.user), status=200)


@api_view(['GET'])
def user_logout(request):
    """
        Delete user's authentication token.
    """
    request.user.auth_token.delete()
    logout(request)
    return Response(status=204)


@api_view(['POST'])
@permission_classes([AllowAny])
def account_token_confirm(request, token):

    data = signing.loads(token)
    user = User.objects.filter(id=data.get('userId')).first()

    if not (data and user and user.account.token == token):
        return Response({'message': 'Token expired'}, status=400)

    if data.get('action') == 'resetPassword':

        form = forms.PasswordForm(request.data)

        if not form.is_valid():
            return Response({'Submitted data is invalid'}, status=400)

        user.account.token = ''
        user.account.save()
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        return Response({'message': 'New password set.'}, status=204)


@api_view(['GET'])
@permission_classes([AllowAny])
def account_token_handle(request, token):

    data = signing.loads(token, max_age=3600)
    user = User.objects.filter(id=data.get('userId')).first()

    if not (data and user and user.account.token == token):
        user.account.token = ''
        user.account.save()
        return redirect(f'{settings.CLIENT_URL}/res/Token%20expired')

    if data.get('action') == 'resetPassword':
        return redirect(f'{settings.CLIENT_URL}/password/reset/{token}')

    elif data.get('action') == 'DELETE':
        user.delete()
        msg = 'Your account has been deleted'.replace(' ', '%20')
        return redirect(f'{settings.CLIENT_URL}/res/{msg}')

    elif data.get('action') == 'activateAccount':
        user.account.token = ''
        user.account.save()
        user.is_active = True
        user.save()
        msg = 'Your account has been activated'.replace(' ', '%20')
        return redirect(f'{settings.CLIENT_URL}/res/{msg}')

    elif data.get('action') == 'updateEmail':
        user.account.token = ''
        user.account.save()
        user.email = data.get('email')
        user.save()
        msg = 'Your new email has been set'.replace(' ', '%20')
        return redirect(f'{settings.CLIENT_URL}/res/{msg}')
