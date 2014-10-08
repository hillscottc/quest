from django.db import models
from django.contrib.auth.models import User
from quizapp.models import CommonModel


class Quiz(CommonModel):
    owner = models.ForeignKey(User, related_name='quiz_owner', null=True, blank=True)
    # user = models.ManyToManyField(User, blank=True, null=True, related_name='quiz_user')
    name = models.CharField(max_length=100, verbose_name="quiz name")
    source = models.CharField(max_length=100, blank=True, null=True, )
    # classroom = models.ForeignKey(Classroom, blank=True, null=True)

    class Meta:
        app_label = 'quizapp'

    def __unicode__(self):
        return self.name


class QuizSession(CommonModel):

    class Meta:
        app_label = 'quizapp'

    quiz = models.ForeignKey(Quiz)
    taker = models.ForeignKey(User, null=True, blank=True)

    EDIT = 'EDIT'
    STUDY = 'STUDY'
    STANDARD = 'STANDARD'
    TRICKY = 'TRICKY'
    TAKE_TYPE_CHOICES = (
        (EDIT, 'Edit'),
        (STUDY, 'Study'),
        (STANDARD, 'Standard'),
        (TRICKY, 'Tricky'))
    take_type = models.CharField(max_length=8, choices=TAKE_TYPE_CHOICES,
                                 default=STUDY, verbose_name="type")

    def __unicode__(self):
        return "%s %s %s" % (self.quiz.name, self.taker, self.take_type)


class Question(CommonModel):
    class Meta:
        app_label = 'quizapp'
    quiz = models.ForeignKey(Quiz, related_name="questions")
    text = models.CharField(max_length=255)
    order = models.IntegerField(null=True, blank=True)
    MULT_CHOICE = 'MC'
    FILLIN = 'FI'
    TRUE_FALSE = 'TF'
    ANS_TYPE_CHOICES = ((MULT_CHOICE, 'Multiple Choice'),
                        (FILLIN, 'Fill in the blank'),
                        (TRUE_FALSE, 'True or False'))
    ans_type = models.CharField(max_length=2, choices=ANS_TYPE_CHOICES,
                                default=MULT_CHOICE, verbose_name="type")

    def __unicode__(self):
        return self.text


class Answer(CommonModel):
    question = models.ForeignKey(Question, related_name="answers")
    text = models.CharField(max_length=99, verbose_name='text')
    notes = models.CharField(max_length=256, blank=True, null=True,
                             verbose_name='notes')
    correct = models.BooleanField(default=False)

    class Meta:
        app_label = 'quizapp'

    def __unicode__(self):
        return u"%s: %s" % (self.question.text, self.text)


__all__ = [
    'Quiz',
    'QuizSession',
    'Question',
    'Answer',
]