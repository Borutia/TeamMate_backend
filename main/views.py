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

from .models import *
from .serializers import *
from .utils import *


class UserProfileView(
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet,
                      NestedViewSetMixin
                      ):
    "Апи для получения информации о профиле"
    permission_classes = [AuthPermission]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @action(detail=True, methods=['get'], serializer_class=ProfileSerializer)
    def user(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=kwargs.get('pk'))
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProjectView(
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet,
                  NestedViewSetMixin
                  ):
    "Апи для получения информации по проектам"
    permission_classes = [AuthPermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    @action(detail=False, methods=['post'], serializer_class=ProjectSerializer)
    def add(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['owner'] = get_user(request)
            # try:
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
            # except Exception:
            #     return Response('При создании проекта произошла ошибка')

    @action(detail=False, methods=['get'], serializer_class=ProjectSerializer)
    def all(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], serializer_class=ProjectSerializer)
    def my(self, request, *args, **kwargs):
        projects = Project.objects.filter(owner=get_user_id(request))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], serializer_class=ProjectSerializer)
    def imember(self, request, *args, **kwargs):
        imembers = Members.objects.filter(user=get_user_id(request))
        projects_id = []
        for member in imembers:
            projects_id.append(member.project.id)
        projects = Project.objects.in_bulk(projects_id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], serializer_class=ProjectSerializer)
    def in_progress(self, request, *args, **kwargs):
        projects = Project.objects.filter(owner=get_user_id(request), status='in_progress')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], serializer_class=ProjectSerializer)
    def finished(self, request, *args, **kwargs):
        projects = Project.objects.filter(owner=get_user_id(request), status='finished')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)



class MembersView(
                  GenericViewSet,
                  NestedViewSetMixin
                  ):
    "Апи для работы с участниками проектов"
    permission_classes = [AuthPermission]
    serializer_class = ProjectMemberSearchSerializer
    queryset = Members.objects.all()

    @action(detail=False, methods=['post'], serializer_class=ProjectMemberSearchSerializer)
    def SearchMembers(self, request, *args, **kwargs):
        serializer = ProjectMemberSearchSerializer(data=request.data)
        if serializer.is_valid():
            project_skills = ProjectSkill.objects.filter(project_id=serializer.data['id'])
            skills = []
            for skill in project_skills:
                skills.append(skill.skill)
            print(str(skills))
            skill_profile = Skill.objects.filter(skill__in=skills)
            profs = []
            for prof in skill_profile:
                profs.append(prof.user)
            profiles = Profile.objects.filter(user__in=profs)
            prf_serializer = ProfileSerializer(profiles, many=True)
            return Response(prf_serializer.data)
        else:
            return Response('Invalid DATA')

    @action(detail=False, methods=['post'], serializer_class=MembersSerializer)
    def add(self, request, *args, **kwargs):
        serializer = MembersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Invalid DATA')

class HeadReviewView(
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet,
                  NestedViewSetMixin
                  ):
    "Апи для отзывов руководителей"
    permission_classes = [AuthPermission]
    serializer_class = HeadReviewSerializer
    queryset = HeadReview.objects.all()

class ProfileRatingView(
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet,
                  NestedViewSetMixin
                  ):
    "Апи для рейтингов пользователей"
    permission_classes = [AuthPermission]
    serializer_class = ProfileRatingSerializer
    queryset = HeadReview.objects.all()
