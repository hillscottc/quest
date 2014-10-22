from django.conf.urls import patterns, url
from django.contrib import admin
from questapp import views

admin.autodiscover()

urlpatterns = patterns(
    '',

    # url(r'^clues/$', views.ClueListView.as_view(), name='clue-list'),
    url(r'^clues/$', views.ClueIndexView.as_view(), name='clue-index'),
    url(r'^clues/page/(?P<page>\d+)/$', views.ClueListView.as_view(), name='clues-paged'),
    url(r'^clues/random/(?P<num>\d+)/$', views.ClueRandomView.as_view(), name='clues-random'),
    url(r'^clue/(?P<pk>[0-9]+)/$', views.ClueDetailView.as_view(), name='clue-detail'),

    url(r'^clues/search/$', views.ClueSearchView.as_view(), name='clue-search'),



    url(r'^cats/$', views.CatListView.as_view(), name='cat-list'),
    url(r'^cats/page/(?P<page>\d+)/$', views.CatListView.as_view(), name='cats-paged'),

)
