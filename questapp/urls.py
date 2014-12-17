from django.conf.urls import patterns, url, include
from django.contrib import admin
from questapp import views
from tastypie.api import Api
from questapp.api import ClueResource, RandomCluesResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ClueResource())
v1_api.register(RandomCluesResource())


urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name='questapp-home'),

    url(r'^bbtest$', views.BBTestView.as_view(), name='bbtest'),

    url(r'^clues/$', views.ClueIndexView.as_view(), name='clues-index'),

    url(r'^clues/random/$', views.ClueRandomView.as_view(), name='clues-random'),

    url(r'^clue/(?P<pk>[0-9]+)/$', views.ClueDetailView.as_view(), name='clue-detail'),

    # url(r'^clues/cat/(?P<cat_id>\d+)/$', views.CluesByCatView.as_view(), name='clues-by-cat'),

    url(r'^clues/search/$', views.ClueSearchView.as_view(), name='clue-search'),

    url(r'^api/', include(v1_api.urls)),

)

# Sample API Urls:
# /api/v1/?format=json
# /api/v1/clue?format=json
# /api/v1/clue/1/?format=json
# /api/v1/random_clues?format=json