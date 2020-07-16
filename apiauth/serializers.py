from rest_framework import serializers
from django.conf import settings
from rest_framework.settings import api_settings
import json
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        read_only_fields=('id',)

class ResetPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model=User
        fields = ('username',)
