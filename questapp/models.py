import logging
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

log = logging.getLogger(__name__)


class BaseModelManager(models.Manager):

    def update(self, **kwargs):
        fieldnames = [field.name for field in self._meta.fields]
        for attr, value in kwargs.iteritems():
            if attr in fieldnames and hasattr(self, attr):
                setattr(self, attr, value)
        self.save()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, editable=False)
    last_accessed = models.DateTimeField(auto_now=True, editable=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True
        ordering = ["-modified"]


class Game(BaseModel):
    sid = models.CharField(primary_key=True, max_length=8, help_text="(Jeapordy) Show id.")
    gid = models.CharField(unique=True, max_length=8, help_text="(External) Game id.",
                           null=True, blank=True)
    title = models.CharField(max_length=250)
    air_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=250)

    class Meta:
        ordering = ["-modified"]

    def __unicode__(self):
        return u"{}".format(self.gid)

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})


class Clue(BaseModel):
    game = models.ForeignKey(Game)
    category = models.CharField(max_length=255)
    question = models.CharField(max_length=355)
    answer = models.CharField(max_length=355)

    class Meta:
        unique_together = ['game', 'category', 'question']
        ordering = ['category', 'question']

    def get_absolute_url(self):
        return reverse('clue-detail', kwargs={'pk': self.pk})

    def desc(self):
        return u"CAT:{} Q:{} A:{}".format(self.category, self.question, self.answer)

    def get_json(self):
        return {'category': self.category.name,
                'question': self.question,
                'answer': self.answer}

    def __unicode__(self):
        return u"Q:{} A:{}".format(self.question, self.answer)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    rights = models.IntegerField(default=0)
    wrongs = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

