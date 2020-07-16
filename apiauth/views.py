import coreapi
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.filters import BaseFilterBackend
from rest_framework import filters

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
import django_filters.rest_framework
from django_filters import FilterSet
from rest_framework import filters
from django_filters.rest_framework import BooleanFilter, ChoiceFilter, NumberFilter
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import *
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings
from django.core.mail import send_mail

class CustomAuthToken(
                      GenericViewSet,
                      ):
    "АПИ для работы с токеном"
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], serializer_class=UserSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)
        user = User.objects.get(username=serializer.data['username'])
        if check_password(serializer.data['password'], user.password):
            token, created = Token.objects.get_or_create(user=user)
            response = Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
            response.set_cookie('TeamAuth', token.key)
            return response
        else:
            return Response({
                'Неправильный логин или пароль'
            })

    @action(detail=False, methods=['post'], serializer_class=UserSerializer)
    def register(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response('Registraion faild')

    @action(detail=False, methods=['post'], serializer_class=ResetPasswordSerializer)
    def sendnewpassword(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data['username'])
            # if user != True:
            #     return Response("User do not exist")
            # User.objects.get(username=serializer.data['username']).update(password="admin1234!a2")
            headers = {'To': 'TeamMate'}
            send_mail('Новый пароль', 'Ваш новый пароль:{}'.format("admin1234!a2"), settings.EMAIL_HOST_USER, [user.email])
            return Response('Новый пароль отправлен на вашу почту')
        else:
            return Response('Error')
