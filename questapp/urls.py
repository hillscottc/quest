from django.conf.urls import patterns, url
from django.contrib import admin
from questapp import views

admin.autodiscover()

urlpatterns = patterns(
    '',

    # url(r'^clues/$', views.ClueListView.as_view(), name='clue-list'),
    url(r'^$', views.HomeView.as_view(), name='questapp-home'),
    url(r'^clues/$', views.ClueListView.as_view(), name='clues-index'),
    url(r'^clues/page/(?P<page>\d+)/$', views.ClueListView.as_view(), name='clues-paged'),
    url(r'^clue/(?P<pk>[0-9]+)/$', views.ClueDetailView.as_view(), name='clue-detail'),

    url(r'^clues/random/(?P<num>\d+)/$', views.ClueRandomView.as_view(), name='clues-random'),
    url(r'^cats/random/(?P<num>\d+)/$', views.CatRandomView.as_view(), name='cats-random'),

    url(r'^clues/search/$', views.ClueSearchView.as_view(), name='clue-search'),

    url(r'^clues/cat/(?P<cat_id>\d+)/$', views.CluesByCatView.as_view(), name='clues-by-cat'),

    url(r'^cats/$', views.CatListView.as_view(), name='cats-index'),
    url(r'^cats/page/(?P<page>\d+)/$', views.CatListView.as_view(), name='cats-paged'),

)
