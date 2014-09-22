from django.conf.urls import patterns, url
from django.contrib import admin
from .views import HomeView, ClueListView, ClueDetailView, CatListView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', HomeView.as_view()),

    url(r'^clues/$',
        ClueListView.as_view(), name='clue-list'),
    url(r'^clues/(?P<pk>[0-9]+)/$',
        ClueDetailView.as_view(), name='clue-detail'),

    url(r'^cats/(?P<num>[0-9]+)/$',
        CatListView.as_view(), name='cat-list'),

)
