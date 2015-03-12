from django.contrib.auth.models import User
from questapp.models import Clue, UserProfile, UserLog
from questapp.cors_base import CORSModelResource, CORSResource
from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from django.conf import settings


class ClueResource(CORSModelResource):

    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'
        excludes = ['game', 'created', 'modified', 'last_accessed']


class RandomCluesResource(CORSModelResource):

    class Meta:
        queryset = Clue.objects.all().order_by('?')[:settings.API_LIMIT_PER_PAGE]
        resource_name = 'random_clues'


class UserResource(CORSModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }


class UserProfileResource(CORSModelResource):

    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_prof'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }


class UserLogResource(CORSModelResource):

    class Meta:
        queryset = UserLog.objects.all()
        resource_name = 'user_log'
        authorization = Authorization()
        filtering = {
            'userid': ALL,
            'questionid': ALL
        }
