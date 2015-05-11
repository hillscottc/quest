from django.conf.urls import patterns, include, url
from django.contrib import admin

import questproj.views as views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^googlefd8980378f4a07d2.html$', views.google_verify),

    url(r'', include('django_stormpath.urls')),

    # url(r'^questapp/', include('questapp.urls')), # put questapp at /questapp
    url(r'^', include('questapp.urls')),            # put questapp at /

    url(r'^admin-page/', views.AdminPageFormView.as_view(), name="admin-page"),

    url(r'^scoreboard', views.ScoreboardView.as_view(), name="scoreboard"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about$', views.AboutView.as_view(), name="about"),

    url(r'^user/account/$', views.UserAccountView.as_view(), name='user_account'),

    )

