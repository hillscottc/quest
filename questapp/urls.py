from django.conf.urls import patterns, url
from django.contrib import admin
from questapp import views

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name='questapp-home'),

    url(r'^bbtest$', views.BBTestView.as_view(), name='bbtest'),


    url(r'^clues/page(?P<page>[0-9]+)/$', views.ClueIndexView.as_view(),  name='clues-index'),
    url(r'^clues/random/$', views.ClueRandomView.as_view(),  name='clues-random'),

    ## Using a RandomView as a deafault for cats index,, instead of a plain list.
    # url(r'^cats/$', views.CatRandomView.as_view(), name='cats-index'),

    url(r'^clue/(?P<pk>[0-9]+)/$', views.ClueDetailView.as_view(), name='clue-detail'),

    # url(r'^clues/cat/(?P<cat_id>\d+)/$', views.CluesByCatView.as_view(), name='clues-by-cat'),

    url(r'^clues/search/$', views.ClueSearchView.as_view(), name='clue-search'),

)
