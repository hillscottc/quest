from django.conf.urls import patterns, include, url
from .views import AboutView, CategoryListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', AboutView.as_view()),
    url(r'^about/', AboutView.as_view()),

)
