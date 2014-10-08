from django.conf.urls import patterns, url
import quizapp.views as views

# from quizapp.admin import quizapp_admin

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),

    url(r'quiz/index/$', views.quiz_index, name='quiz_index'),
    url(r'quiz/take/(?P<quiz_id>\d+)/$', views.quiz_take, name='quiz_take'),
    url(r'quiz/delete/(?P<quiz_id>\d+)/$', views.quiz_delete, name="quiz_delete"),
    # url(r'quiz/add/$', views.quiz_add, name="quiz_add"),
    url(r'quiz/edit/(?P<quiz_id>\d+)/$', views.quiz_edit, name='quiz_edit'),


    url(r'question/detail/(?P<question_id>\d+)/$', views.question_detail, name='quiz_detail'),


    url(r'answer/post/(?P<a_id>\d+)/$', views.answer_post, name='answer_post'),
    url(r'question/edit/(?P<question_id>\d+)/$', views.question_edit, name='question_edit'),
    # url(r'answer/add/(?P<question_id>\d+)/$', 'quizapp.answer.views.answer_add', name='answer_add'),

    url(r'question/add/(?P<question_id>\d+)/$', views.question_add, name='question_add'),

    url(r'log/$', views.log_view, name="log"),
    # url(r'admin/', include(quizapp_admin.urls)),
)
