import logging
from django.db import models
from django.core.urlresolvers import reverse
from .models_base import BaseModel

log = logging.getLogger(__name__)


def get_relevant_counts():
    return {'Game': Game.objects.count(),
            'Clue': Clue.objects.count(),
            'Category': Category.objects.count()}


class Game(BaseModel):
    sid = models.CharField(primary_key=True, max_length=8, help_text="(Jeapordy) Show id.")
    gid = models.CharField(unique=True, max_length=8, help_text="(External) Game id.",
                           null=True, blank=True)
    title = models.CharField(max_length=250)

    class Meta:
        ordering = ["-modified"]
        unique_together = ['gid', 'sid']

    def __unicode__(self):
        return u"%s-%s" % (self.gid, self.sid)

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})


class Category(BaseModel):
    """A category in a game. Names unique per game, not globally unique.
    Also contains info about column and round."""
    game = models.ForeignKey(Game)
    round_num = models.SmallIntegerField(default=0)
    col_num = models.SmallIntegerField(default=0)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['game', 'round_num', 'col_num']
        ordering = ['round_num', 'col_num']

    def __unicode__(self):
        return u"%s-%s-%s-%s" % (self.game, self.round_num, self.col_num, self.name)

    def get_absolute_url(self):
        return reverse('cat-detail', kwargs={'pk': self.pk})


class Clue(BaseModel):
    category = models.ForeignKey(Category)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    class Meta:
        unique_together = ['category', 'question']
        ordering = ['category', 'question']

    def get_absolute_url(self):
        return reverse('clue-detail', kwargs={'pk': self.pk})

    def desc(self):
        return u"CAT:{} Q:{} A:{}".format(self.category, self.question, self.answer)

    def __unicode__(self):
        return u"Q:{} A:{}".format(self.question, self.answer)
