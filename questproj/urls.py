from django.conf.urls import patterns, include, url
from django.contrib import admin

import questproj.views as views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^googlefd8980378f4a07d2.html$', views.google_verify),

    # url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^$', views.IndexView.as_view(), name="home"),

    # url(r'^questapp/', include('questapp.urls')), # put questapp at /questapp
    url(r'^', include('questapp.urls')),            # put questapp at /

    url(r'^admin-page/', views.AdminPageFormView.as_view(), name="admin-page"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about$', views.AboutView.as_view(), name="about"),
    url(r'^test-mari$', views.TestMariView.as_view(), name="test-mari"),


    (r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^user/account/$', views.UserAccountView.as_view(), name='user_account'),
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'}, name="password_reset"),

    (r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),

    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': '/user/password/done/'}),

    (r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    )

