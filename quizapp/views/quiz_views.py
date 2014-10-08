from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput
from django.contrib import messages
from django.forms.models import inlineformset_factory
from quizapp.models import Quiz, Question, QuizSession
from quizapp.forms import QuizSessionForm, QuizForm
from quizapp.quiz_mgr import log_message
from .common_views import custom_context_proc
from django.template import RequestContext


def quiz_index(request):
    """List all quizzes."""
    return render(request, 'quiz/index.html',
                  {'quiz_list': Quiz.objects.all().order_by('-updated_at')},
                  context_instance=RequestContext(request, processors=[custom_context_proc]))


@login_required
def quiz_add(request):
    if request.method == 'POST':
        form = QuizForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz addded.')

            return HttpResponseRedirect(reverse('quiz_index'))
    else:
        form = QuizForm(initial={'user': request.user})
        form.fields['user'].widget = HiddenInput()

    return render(request, 'quiz/add.html',
                  {'form': form},
                  context_instance=RequestContext(request, processors=[custom_context_proc]))


@login_required
def quiz_delete(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.delete()
    messages.success(request, 'Quiz deleted.')
    return HttpResponseRedirect(reverse('quiz_index'))


@login_required
def quiz_edit(request, quiz_id):
    """Manage set of answers"""
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        QuestionFormSet = inlineformset_factory(Quiz, Question)
        return HttpResponse("handle edit")
        # formset = QuestionFormSet(request.POST, request.FILES, instance=quiz)
        # if formset.is_valid():
        #     # do something with the formset.cleaned_data?
        #     formset.save()
        #     messages.success(request, 'Questions updated.')
        #     # return HttpResponseRedirect(reverse('quizapp:questions_manage', args=(quiz_id,)))
    else:
        if request.user.is_authenticated():
            taker = request.user
        else:
            taker = None
        ses = QuizSession.objects.create(taker=taker, quiz=quiz, take_type=QuizSession.EDIT)
        form = QuizSessionForm(instance=ses)
        return render(request, 'quiz/detail.html',
                      {'form': form,
                       'questions': quiz.questions.all(),
                       'back_to_url': reverse('quiz_index'),
                       'q_list': quiz.questions.all()},
                      context_instance=RequestContext(request, processors=[custom_context_proc]))


def quiz_take(request, quiz_id):
    """List questions for quiz."""
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        form = QuizSessionForm(request.POST)
        if request.POST.get("test_result", "") == 'CORRECT':
            log_message(message="COMPLETED", taker=request.user, quiz=quiz)
            # messages.success(request, 'Congratulations! Your results have been added to the board.')
            # return HttpResponseRedirect(reverse('quiz_index'))
            return render(request, 'splash.html',
                          {'heading': "Congratulations!",
                           'lead': "Your results have been added to the board.",
                           'go_to': reverse('quiz_index')},
                          context_instance=RequestContext(request, processors=[custom_context_proc]))
        else:
            resp = []
            for k in request.POST.keys():
                if 'q_id_' in k:
                    resp.append((k, request.POST[k]))

            return HttpResponse("TODO: I've got the q's and a's. Process: %s" % resp)

    else:
        if request.user.is_authenticated():
            taker = request.user
        else:
            taker = None
        ses = QuizSession.objects.create(taker=taker, quiz=quiz)

        # form = QuizSessionForm(initial={'taker': taker, 'quiz': quiz})
        form = QuizSessionForm(instance=ses)
        log_message(message="STARTED", taker=request.user, quiz=quiz)
        return render(request, 'quiz/detail.html',
                      {'form': form,
                       'questions': quiz.questions.all(),
                       'back_to_url': reverse('quiz_index'),
                       'q_list': quiz.questions.all()},
                      context_instance=RequestContext(request, processors=[custom_context_proc]))


__all__ = [
    'quiz_index',
    'quiz_add',
    'quiz_delete',
    'quiz_edit',
    'quiz_take',
]