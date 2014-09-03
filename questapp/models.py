import logging
from django.db import models
from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)


class BaseModelManager(models.Manager):

    def upsert(self, **kwargs):
        """Insert or update.
        Usage: x.upsert(name='joe', defaults=dict(id=1))
        """
        obj, created = self.get_or_create(**kwargs)
        if not created and "defaults" in kwargs:
            for k, v in kwargs.get("defaults", {}).items():
                if k not in dir(obj):
                    raise AttributeError(
                        "Bad attr {} for update on {} ({})".format(
                            k, type(obj), obj.pk))
                setattr(obj, k, v)
            obj.save()

        if created:
            log.debug("Created {}.".format(obj))
        else:
            log.debug("Updated {}.".format(obj))

        return obj, created

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
    show_num = models.SmallIntegerField(primary_key=True)
    game_id = models.SmallIntegerField(null=True, blank=True,
                                       help_text="id assigned by data host.")

    class Meta:
        ordering = ["-modified"]

    def __unicode__(self):
        return unicode(self.show_num)


class Category(BaseModel):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['game', 'name']
        ordering = ["name"]

    def __unicode__(self):
        return unicode(self.name)


class Clue(BaseModel):
    game = models.ForeignKey(Game, null=True, blank=True)
    category = models.ForeignKey(Category)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    level = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ['game', 'question']
        ordering = ['game', 'category', 'level', 'question']

    def get_absolute_url(self):
        return reverse('clue-detail', kwargs={'pk': self.pk})

    def desc(self):
        return u"CAT:{} Q:{} A:{}".format(self.category, self.question, self.answer)

    def __unicode__(self):
        return u"Q:{} A:{}".format(self.question, self.answer)
