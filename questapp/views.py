from datetime import date
from django.conf import settings
from django.views.generic import TemplateView
from questapp.utils import dbstore_get
from questapp.models import UserLog, Clue


def get_counts(user):
    counts = {}
    if user.username:
        counts['user_today'] = UserLog.objects.filter(created__gte=date.today(),
                                                      userid=user.id).count()
        counts['user_alltime'] = UserLog.objects.filter(userid=user.id).count()
    else:
        counts['user_today'] = '-'
        counts['user_alltime'] = '-'

    counts['everyone_today'] = UserLog.objects.filter(created__gte=date.today()).count()
    counts['everyone_alltime'] = UserLog.objects.count()
    return counts


class CluesView(TemplateView):
    template_name = "clues.html"

    def get_context_data(self, **kwargs):
        context = super(CluesView, self).get_context_data(**kwargs)

        clues = None
        cat = self.kwargs.get('cat')

        if cat:
            clues = Clue.objects.filter(category=self.kwargs.get('cat'))

        context.update({'api_limit': settings.API_LIMIT_PER_PAGE,
                        'clues': clues,
                        'cat': cat,
                        'answer_tracking': dbstore_get('answer_tracking', False)})
        if dbstore_get('answer_tracking', True):
            context.update(get_counts(self.request.user))
        return context