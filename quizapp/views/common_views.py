from django.shortcuts import render
from ..models import Quiz, RawLog, QuizSession
from django.conf import settings
from django.template import RequestContext


def custom_context_proc(request):
    """A context processor that provides vars for base template."""
    nav_take_my = None
    nav_edit_my = None
    if request.user.is_authenticated():
        pass
        # nav_take_my = Quiz.objects.filter(user=user).order_by('-updated_at')[:5]
        # nav_edit_my = Quiz.objects.filter(owner=user).order_by('-updated_at')[:5]

    return {
        'SITE_NAME': settings.SITE_NAME,
        'nav_take_my': nav_take_my,
        'nav_take_all': Quiz.objects.all()[:5],
        'nav_edit_my': nav_edit_my
    }


def home(request):
    return render(request, 'home.html',
                  context_instance=RequestContext(request, processors=[custom_context_proc]))


def log_view(request):
    """The log page."""
    all_log = RawLog.objects.all().order_by('-created_at')[:50]

    if request.user.is_authenticated():
        my_quiz_log = QuizSession.objects.filter(
            taker=request.user).order_by('-updated_at')[:50]
    else:
        my_quiz_log = None

    return render(request, 'log.html',
                  {'all_log': all_log, 'my_quiz_log': my_quiz_log},
                  context_instance=RequestContext(request, processors=[custom_context_proc]))


__all__ = [
    'home',
    'log_view',
]