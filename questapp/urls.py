from django.conf.urls import patterns, url, include
from django.contrib import admin
from tastypie.api import Api
from questapp.api import (ClueResource, RandomCluesResource,
                          UserResource, UserProfileResource)

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ClueResource())
v1_api.register(RandomCluesResource())
v1_api.register(UserResource())
v1_api.register(UserProfileResource())


urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),
)

