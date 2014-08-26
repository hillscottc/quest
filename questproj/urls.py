from django.conf.urls import patterns, include, url
from questapp.views import AboutView, CategoryListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', AboutView.as_view()),

    url(r'^questapp/', include('questapp.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
