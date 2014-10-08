from django.conf.urls import patterns, include, url
from django.contrib import admin
from questapp.views import HomeView
from quizapp.registration.views import register, user_login, user_account

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view()),
    url(r'^questapp/', include('questapp.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    ## From quzapp.....
    url(r'^user/account/$', user_account, name='user_account'),
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
     'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
     'django.contrib.auth.views.password_reset_confirm',
     {'post_reset_redirect': '/user/password/done/'}),
    (r'^user/password/done/$',
     'django.contrib.auth.views.password_reset_complete'),

    url(r'^quizapp/', include('quizapp.urls')),


)
