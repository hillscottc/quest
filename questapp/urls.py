from django.conf.urls import patterns, url
from django.contrib import admin
from .views import ClueListView, ClueDetailView, CatListView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^clues/$', ClueListView.as_view(), name='clue-list'),
    url(r'^clues/page/(?P<page>\d+)/$', ClueListView.as_view(), name='clues-paged'),
    url(r'^clue/(?P<pk>[0-9]+)/$', ClueListView.as_view(), name='clue-detail'),

    url(r'^cats/$', CatListView.as_view(), name='cat-list'),
    url(r'^cats/page/(?P<page>\d+)/$', CatListView.as_view(), name='cats-paged'),

)
