from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Clue, Category
from .forms import TestForm
from questproj.utils import get_random_objs
from questproj.views import BaseTemplateView, BaseDetailView, BaseListView, BaseFormView


class TestFormView(BaseFormView):
    template_name = "test.html"
    form_class = TestForm

    def form_valid(self, form):
        cd = form.cleaned_data
        msg = None
        if cd['test_txt']:
            msg = "You said " + cd['test_txt']

        context = self.get_context_data(form=form)
        if msg:
            context.update({'test_msg': msg})
        return self.render_to_response(context)
        # return super(TestFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('test-form')


class HomeView(BaseTemplateView):
    template_name = "home.html"


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
    template_name = 'clue_list.html'
    queryset = Clue.objects.all()
    paginate_by = 10


class ClueRandomView(BaseListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'

    def get_queryset(self):
        output = list(get_random_objs(Clue, int(float(self.kwargs['num']))))
        return output


class CatListView(BaseListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'
    queryset = Category.objects.all()
    paginate_by = 10

