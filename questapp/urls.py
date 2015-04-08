from django.conf.urls import patterns, url, include
from django.contrib import admin
import views
from tastypie.api import Api
from questapp.api import (ClueResource, RandomCluesResource,
                          UserResource, UserProfileResource, UserLogResource)

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ClueResource())
v1_api.register(RandomCluesResource())
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(UserLogResource())


urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', views.HomeView.as_view(), name="home"),

    url(r'^clues/$', views.CluesView.as_view(), name="clues"),

    url(r'^clues/cat/(?P<cat>.+)$', views.CluesView.as_view(), name="clues-by-cat"),

)

