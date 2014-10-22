from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Clue, Category
from .forms import ClueSearchForm
from questproj.utils import get_random_objs
from questproj.views import BaseTemplateView, BaseDetailView, BaseListView, BaseFormView


class HomeView(BaseTemplateView):
    template_name = "home.html"


class ClueIndexView(BaseTemplateView):
    template_name = "clue_index.html"


class ClueDetailView(BaseDetailView):
    context_object_name = 'clue'
    queryset = Clue.objects.all()
    template_name = "clue_detail.html"

    def get_object(self):
        object = super(ClueDetailView, self).get_object()
        # Record the last accessed date
        object.last_accessed = timezone.now()
        object.save()
        return object


class ClueListView(BaseListView):
    context_object_name = 'clue_list'
    template_name = 'clue_paged_list.html'
    queryset = Clue.objects.all()
    paginate_by = 10


class ClueRandomView(BaseListView):
    context_object_name = 'clue_list'
    template_name = 'clue_paged_list.html'

    def get_queryset(self):
        output = list(get_random_objs(Clue, int(float(self.kwargs['num']))))
        return output


class CatListView(BaseListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'
    queryset = Category.objects.all()
    paginate_by = 10


class ClueSearchView(BaseFormView):
    template_name = "clue_search.html"
    form_class = ClueSearchForm

    def form_valid(self, form):
        cd = form.cleaned_data
        context = self.get_context_data(form=form)

        if not cd['search_txt']:
            msg = "All recs."
            qs = Clue.objects.all()
        else:
            msg = "Searching by: " + cd['search_txt']
            qs = Clue.objects.filter(question__contains=cd['search_txt'])

        # I'd prefer to use pagination.....somehow use the ListView way.
        max_recs = 20
        clue_list = qs[:max_recs]

        context.update({'test_msg': msg})
        context.update({'clue_list': clue_list})
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('clue-search')