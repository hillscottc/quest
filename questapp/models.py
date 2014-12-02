import logging
from django.db import models
from django.core.urlresolvers import reverse
from .models_base import BaseModel

log = logging.getLogger(__name__)


def get_relevant_counts():
    return {'Game': Game.objects.count(),
            'Clue': Clue.objects.count(),
            'Category': Category.objects.count()}


def get_empty_cats():
    """Get Categories with no questions. Somewtimes they get through the parser.
    Usually one would delete them, as a clenaup.
    """
    for cat in Category.objects.all():
        if not cat.clue_set.exists():
            yield cat


class Game(BaseModel):
    sid = models.CharField(primary_key=True, max_length=8, help_text="(Jeapordy) Show id.")
    gid = models.CharField(unique=True, max_length=8, help_text="(External) Game id.",
                           null=True, blank=True)
    title = models.CharField(max_length=250)
    air_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=250)

    class Meta:
        ordering = ["-modified"]
        unique_together = ['gid', 'sid']

    def __unicode__(self):
        return u"%s-%s" % (self.gid, self.sid)

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})


class Round(BaseModel):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ['game', 'name']

    def __unicode__(self):
        return self.name


class Category(BaseModel):
    round = models.ForeignKey(Round)
    name = models.CharField(max_length=100)


    class Meta:
        unique_together = ['round', 'name']
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})


class Clue(BaseModel):
    # game = models.ForeignKey(Game)
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


