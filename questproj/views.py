from django.shortcuts import render
from django.conf import settings
from django.template import RequestContext


def base_context(request):
    """A context processor that provides vars for base template."""
    if request.user.is_authenticated():
        pass

    return {
        'SITE_NAME': settings.SITE_NAME,
    }


def home(request):
    context = RequestContext(request, processors=[base_context])
    return render(request, 'home.html', context_instance=context)
