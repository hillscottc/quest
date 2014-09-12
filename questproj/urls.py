from django.conf.urls import patterns, include, url
from django.contrib import admin
from questapp.views import HomeView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view()),
    url(r'^questapp/', include('questapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
