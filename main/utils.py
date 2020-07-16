import datetime
import functools

from rest_framework import permissions

from django.conf import settings

from rest_framework.exceptions import (
    AuthenticationFailed, PermissionDenied
)
from .models import *
from rest_framework.authtoken.models import Token

def get_user_id(request):
    token = Token.objects.get(key=get_token(request))
    return token.user_id

def get_token(request):
    token = request.COOKIES.get('TeamAuth')
    return token

def get_user(request):
    user_data = User.objects.get(id=get_user_id(request))
    return user_data

class AuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if get_user_id(request) > 0:
            return view
        raise PermissionDenied(
            'Пользователь не авторизован'
        )
