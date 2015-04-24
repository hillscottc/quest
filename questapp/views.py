import json
from django.conf import settings
from django.views.generic import TemplateView
from questapp.utils import dbstore_get
from questapp.models import UserLog, Clue
from django.http import HttpResponse


class CluesView(TemplateView):
    template_name = "clues.html"

    def get_context_data(self, **kwargs):
        context = super(CluesView, self).get_context_data(**kwargs)

        cat = kwargs.get('cat')
        context.update({'cat': kwargs.get('cat')})

        if cat:
            context.update({'clues': Clue.objects.filter(category=kwargs.get('cat'))})

        context.update({'answer_tracking': dbstore_get('answer_tracking', False)})

        return context


class TestView(TemplateView):
    template_name = "test.html"


def userlog_post(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = json.loads(request.body)
            ul = UserLog.objects.create(**json_data)
            print 'created:', ul
    return HttpResponse("OK")


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({'cats': Clue.get_random_cats(20)})
        return context
