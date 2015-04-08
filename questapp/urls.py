from django.conf.urls import patterns, url
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name="home"),

    url(r'^clues/$', views.CluesView.as_view(), name="clues"),

    url(r'^clues/cat/(?P<cat>.+)$', views.CluesView.as_view(), name="clues-by-cat"),

)

