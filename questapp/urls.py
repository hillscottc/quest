from django.conf.urls import patterns, url
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name="home"),

    url(r'^clues/$', views.CluesView.as_view(), name="clues"),

    url(r'^test$', views.TestView.as_view(), name="test"),

    url(r'^userlog/post$', views.userlog_post, name="userlog_post"),

    url(r'^clues/cat/(?P<cat>.+)$', views.CluesView.as_view(), name="clues-by-cat"),

)

