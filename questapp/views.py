from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Clue, Category
from .forms import ClueSearchForm
from questproj.utils import get_random_objs
from questproj.views import BaseTemplateView, BaseDetailView, BaseListView, BaseFormView


class HomeView(BaseTemplateView):
    template_name = "questapp_home.html"


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
        num = int(float(self.kwargs['num']))
        output = list(get_random_objs(Clue, num))
        return output


class CatRandomView(BaseListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'

    def get_queryset(self):
        num = int(float(self.kwargs['num']))
        output = list(get_random_objs(Category, num))
        return output


class CluesByCatView(BaseListView):
    context_object_name = 'clue_list'
    template_name = 'clue_paged_list.html'

    def get_context_data(self, *args, **kwargs):

        cat_id = int(float(self.kwargs['cat_id']))
        cat = Category.objects.get(id=cat_id)

        context = super(CluesByCatView, self).get_context_data(*args, **kwargs)
        context.update({'search_title': 'Clues By Category'})
        context.update({'cat': cat})
        return context

    def get_queryset(self):
        cat_id = int(float(self.kwargs['cat_id']))
        cat = Category.objects.get(id=cat_id)
        qs = Clue.objects.filter(category=cat)
        return qs.all()


class CatListView(BaseListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


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
        max_recs = 50
        clue_list = qs[:max_recs]

        context.update({'test_msg': msg})
        context.update({'clue_list': clue_list})
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('clue-search')