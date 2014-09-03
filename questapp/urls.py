from django.conf.urls import patterns, include, url
from .views import AboutView, ClueListView, ClueDetailView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^clues/$', ClueListView.as_view()),

    url(r'^clues/(?P<pk>[0-9]+)/$',
        ClueDetailView.as_view(), name='clue-detail'),

)
