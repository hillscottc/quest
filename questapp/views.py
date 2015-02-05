from django.core.urlresolvers import reverse
from django.views.generic import FormView
from .models import Clue
from .forms import ClueSearchForm


class ClueSearchView(FormView):
    context_object_name = 'clue_list'
    template_name = "questapp/clue_search.html"
    form_class = ClueSearchForm
    paginate_by = 20

    def form_valid(self, form):
        cd = form.cleaned_data
        context = self.get_context_data(form=form)

        if not cd['search_txt']:
            msg = "All recs."
            qs = Clue.objects.all()
        else:
            msg = "Searching by: " + cd['search_txt']
            qs = Clue.objects.filter(question__contains=cd['search_txt'])

        max_recs = 50
        clue_list = qs[:max_recs]

        context.update({'test_msg': msg})
        context.update({'list_type': 'clues-search'})
        context.update({'clue_list': clue_list})
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('clue-search')



