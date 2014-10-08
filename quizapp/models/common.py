from django.db import models
from django.contrib.auth.models import User


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'quizapp'


class QuizLog(CommonModel):
    """Log with foreign keys"""
    # quiz = models.ForeignKey(Quiz)
    taker = models.ForeignKey(User, null=True)
    MSG_TYPES = (('STARTED', 'STARTED'), ('COMPLETED', 'COMPLETED'))
    message = models.CharField(max_length=10, choices=MSG_TYPES)

    class Meta:
        app_label = 'quizapp'


class RawLog(CommonModel):
    """Log without foreign keys"""
    message = models.CharField(max_length=100)

    class Meta:
        app_label = 'quizapp'

    def __unicode__(self):
        return u"%s %s" % (self.created_at.strftime('%c'),
                           self.message)

__all__ = ['CommonModel',
           'QuizLog',
           'RawLog',
           ]








