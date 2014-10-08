from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from quizapp.forms import QuestionForm, AnswerFormSet
from quizapp.models import Question, Answer
from .common_views import custom_context_proc
from django.template import RequestContext


def answer_post(request, a_id):
    """Answer a question."""
    answer = Answer.objects.get(pk=a_id)
    if answer.correct:
        response = "<strong>Correct!</strong> Great job."
    else:
        response = "<strong>Sorry,</strong> wrong answer."
    return HttpResponse(response)


@login_required
def question_add(request, quiz_id):
    return render(request, 'quizapp/home.html',
                  context_instance=RequestContext(request, processors=[custom_context_proc]))

# formset = AnswerFormSet(queryset=Answer.objects.filter(question=question))


def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Answers added.')
            return HttpResponseRedirect(
                reverse('question_detail', args=(question_id,)))

    else:
        form = QuestionForm(initial={'question': question})
        # form.fields['question'].widget = HiddenInput()
    return render(request, 'question/detail.html',
                  {'form': form},
                  context_instance=RequestContext(request, processors=[custom_context_proc]))


@login_required
def question_edit(request, question_id):
    question = Question.objects.get(pk=question_id)
    # formset = AnswerFormSet()
    if request.method == 'POST':
        # q_form = QuestionForm(request.POST or None, request.FILES or None)
        q_form = QuestionForm(initial={'question': question})
        formset = AnswerFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data?
            formset.save()
            # messages.success(request, 'Answers updated.')
            return HttpResponseRedirect(reverse('quiz_edit', args=(question.quiz.id,)))

    else:
        q_form = QuestionForm(initial={'text': question.text,
                                       'ans_type': question.ans_type})
        formset = AnswerFormSet(queryset=Answer.objects.filter(question=question))
    return render(request, 'question/edit.html',
                  {'question': question,
                   'q_form': q_form,
                   'back_to_url': reverse('quiz_edit',
                                          args=[question.quiz.id]),
                   # 'add_url': reverse('answer_add',
                   #                    args=[question_id]),
                   # 'delete_url': reverse('quizapp:quiz_delete',
                   #                       args=[quiz_id]),
                   'formset': formset},
                  context_instance=RequestContext(request, processors=[custom_context_proc]))


__all__ = [
    'answer_post',
    'question_add',
    'question_detail',
    'question_edit',
]




# @login_required
# def question_add(request, quiz_id):
#     quiz = Quiz.objects.get(pk=quiz_id)
#     if request.method == 'POST':
#         form = QuestionForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Questions added.')
#             return HttpResponseRedirect(reverse('quiz_edit',
#                                                 args=(quiz_id,)))
#     else:
#         form = QuestionForm(initial={'quiz': quiz,
#                                      'user': request.user})
#         form.fields['quiz'].widget = HiddenInput()
#
#     return render(request, 'question/add.html',
#                   {'quiz': quiz, 'form': form})

# @login_required
# def answer_add(request, question_id):
#     return render(request, 'home.html', {})



