from django.contrib.auth.models import User
from questapp.models import Clue, UserProfile
from questapp.cors_base import CORSModelResource
from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
# Note: API_LIMIT_PER_PAGE is set in settings/base.py


class ClueResource(CORSModelResource):

    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'


class RandomCluesResource(CORSModelResource):

    class Meta:
        queryset = Clue.objects.all().order_by('?')[:100]
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
