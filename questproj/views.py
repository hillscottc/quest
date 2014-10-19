from django.shortcuts import render
from django.conf import settings
from django.template import RequestContext
from django.views.generic import ListView, DetailView, FormView
from django.views.generic import TemplateView


BASE_CONTEXT = {
    'SITE_NAME': settings.SITE_NAME,
}


def base_context(request):
    """The project's func-based home view needs this available in this way."""
    return BASE_CONTEXT


def home(request):
    """The project's home view."""
    context = RequestContext(request, processors=[base_context])
    return render(request, 'home.html', context_instance=context)


class BaseDetailView(DetailView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseDetailView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)
        return context


class BaseTemplateView(TemplateView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)

        return context


class BaseListView(ListView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseListView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)

        return context


class BaseFormView(FormView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseFormView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)

        return context
