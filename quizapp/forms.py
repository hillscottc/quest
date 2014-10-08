from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from quizapp.models import Question, Quiz, QuizSession, Answer
from django.contrib.auth.models import User
from quizapp.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = ('website', 'picture')
        fields = ('website',)


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', 'ans_type')
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # self.fields['text'].label = 'Question text:'
        # if not user.is_authenticated():
        #     pass


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        # fields = ('user', 'organization', 'name', 'questions')


class QuizSessionForm(forms.ModelForm):
    class Meta:
        model = QuizSession
        fields = ('quiz', 'taker', 'take_type')

    def __init__(self, *args, **kwargs):
        super(QuizSessionForm, self).__init__(*args, **kwargs)
        # self.fields['quiz'] = forms.CharField(
        #     widget=forms.TextInput(attrs={'readonly': 'readonly'}))


# AnswerFormSet = inlineformset_factory(Question, Answer)
AnswerFormSet = modelformset_factory(
    Answer,
    fields=('text', ),
    widgets = {'text': forms.Textarea(attrs={'cols': 80, 'rows': 1}), },
    can_delete=True,
    can_order=True,
    extra=1)


# QAFormSet = modelformset_factory(
#     QuestionAnswer,
#     fields=('answer', 'correct'),
#     can_delete=True,
#     # can_order=True,
#     extra=0
# )
# QuestionFormSet = inlineformset_factory(Question, QuestionAnswer)
# QuizFormSet = inlineformset_factory(Quiz, Question)
# QuestionFormSet = modelformset_factory(
#     Question,
#     fields=('text', 'answer_type'),
#     widgets = {'text': Textarea(attrs={'cols': 80, 'rows': 1}), },
#     can_delete=True,
#     # can_order=True,
#     extra=0
# )
