from rest_framework import serializers
from django.conf import settings
from rest_framework.settings import api_settings
import json

from .models import *
from .utils import *


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('id',)

class PersonalQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalQuality
        fields = '__all__'
        read_only_fields = ('id','user')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ('id','user')

class UserResorceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResorce
        fields = '__all__'
        read_only_fields = ('user','id')

class WorkPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlace
        fields = '__all__'
        read_only_fields = ('id','user')

class ProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, required=False)
    skill = SkillSerializer(many=True, required=False)
    personal_quality = PersonalQualitySerializer(many=True, required=False)
    work_place = WorkPlaceSerializer(many=True, required=False)
    education_r = serializers.SerializerMethodField()
    skill_r = serializers.SerializerMethodField()
    quality_r =  serializers.SerializerMethodField()
    work_place_r = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        serializer = HeadReviewSerializer(HeadReview.objects.filter(user=obj.user), many=True)
        return serializer.data

    def get_education_r(self, obj):
        serializer = EducationSerializer(Education.objects.filter(user=obj.user), many=True)
        return serializer.data

    def get_skill_r(self, obj):
        serializer = SkillSerializer(Skill.objects.filter(user=obj.user), many=True)
        return serializer.data

    def get_quality_r(self, obj):
        serializer = PersonalQualitySerializer(PersonalQuality.objects.filter(user=obj.user), many=True)
        return serializer.data

    def get_work_place_r(self, obj):
        serializer = WorkPlaceSerializer(WorkPlace.objects.filter(user=obj.user), many=True)
        return serializer.data

    def create(self, validated_data):
        if 'education' in validated_data:
            educations = validated_data.pop('education')
        else:
            educations = list()
        if 'skill' in validated_data:
            skills = validated_data.pop('skill')
        else:
            skills = list()
        if 'personal_quality' in validated_data:
            qualitys = validated_data.pop('personal_quality')
        else:
            qualitys = list()
        if 'work_place' in validated_data:
            places = validated_data.pop('work_place')
        else:
            places = list()

        profile = Profile.objects.create(**validated_data)

        for education in educations:
            Education.objects.create(**education)
        for skill in skills:
            Skill.objects.create(user_id=profile.user.id, skill=skill['skill'])
        for quality in qualitys:
            PersonalQuality.objects.create(user_id=profile.user.id, quality=quality['quality'])
        return profile
        for place in places:
            WorkPlace.objects.create(user_id=profile.user.id,
                                     country=place['country'],
                                     town=place['town'],
                                     organization=place['organization'],
                                     position=place['position'],
                                     work_start=place['work_start'],
                                     work_end=place['work_end'],
                                     )
        return profile
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('rating','id','education_r', 'skill_r', 'quality_r', 'work_place_r')

class ProjectResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectResource
        fields = '__all__'
        read_only_fields = ('id','project')

class ProjectQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectQuality
        fields = '__all__'
        read_only_fields = ('id' , 'project')

class ProjectSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSkill
        fields = '__all__'
        read_only_fields = ('id' , 'project')

class ProjectSerializer(serializers.ModelSerializer):
    project_quality = ProjectQualitySerializer(many=True, required=False)
    project_skill = ProjectSkillSerializer(many=True, required=False)
    project_resource = ProjectResourceSerializer(many=True, required=False)
    project_skill_r = serializers.SerializerMethodField()
    project_quality_r = serializers.SerializerMethodField()
    project_resource_r = serializers.SerializerMethodField()

    def get_project_skill_r(self, obj):
        serializer = ProjectSkillSerializer(ProjectSkill.objects.filter(project=obj.id), many=True)
        return serializer.data

    def get_project_quality_r(self, obj):
        serializer = ProjectQualitySerializer(ProjectQuality.objects.filter(project=obj.id), many=True)
        return serializer.data

    def get_project_resource_r(self, obj):
        serializer = ProjectResourceSerializer(ProjectResource.objects.filter(project=obj.id), many=True)
        return serializer.data

    def create(self, validated_data):
        if 'project_quality' in validated_data:
            qualitys = validated_data.pop('project_quality')
        else:
            qualitys = list()
        if 'project_skill' in validated_data:
            skills = validated_data.pop('project_skill')
        else:
            skills = list()
        if 'project_resource' in validated_data:
            resorces = validated_data.pop('project_resource')
        else:
            skills = list()
        project = Project.objects.create(**validated_data)
        for quality in qualitys:
            ProjectQuality.objects.create(project_id=project.id, quality=quality['quality'])
        for skill in skills:
            ProjectSkill.objects.create(project_id=project.id, skill=skill['skill'])
        for resorce in resorces:
            ProjectResource.objects.create(project_id=project.id,
                                           type=resorce['type'],
                                           dsc=resorce['dsc'],
                                           )
        return project

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('owner','id', 'project_skill', 'project_quality_r', 'project_resource_r')

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields=('id',)

class MembersProfileSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.id')
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id',)

class ProjectMemberSearchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Project
        fields = ('id',)

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'
        read_only_fields = ('id',)

class HeadReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadReview
        fields = '__all__'
        read_only_fields = ('id',)

class ProfileRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileRating
        fields = '__all__'
        read_only_fields = ('id',)
