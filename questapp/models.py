import logging
from django.db import models
from questapp.utils import trim

log = logging.getLogger(__name__)


class UpsertManager(models.Manager):
    """Provides the upsert method for regular managers.
    Creates the object if it doesn't exist.
    If it exists, update it with the specified defaults.
    Usage: x.upsert(id=1, defaults=dict(name='joe', addr='abc'))
    """
    def upsert(self, **kwargs):
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


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, editable=False)

    objects = UpsertManager()

    class Meta:
        abstract = True

    def update(self, **kwargs):
        fieldnames = [field.name for field in self._meta.fields]
        for attr, value in kwargs.iteritems():
            if attr in fieldnames and hasattr(self, attr):
                setattr(self, attr, value)
        self.save()


class Game(BaseModel):
    show_num = models.SmallIntegerField(primary_key=True)
    game_id = models.SmallIntegerField(null=True, blank=True,
                                       help_text="id assigned by data host.")

    def __unicode__(self):
        return "Game {}".format(self.show_num)


class Clue(BaseModel):
    game = models.ForeignKey(Game, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    class Meta:
        unique_together = ['game', 'question', 'answer', 'category']

    def desc(self):
        return " C:{} Q:{} A:{}".format(self.category, trim(self.question), trim(self.answer))

    def __unicode__(self):
        return "Clue {}".format(self.pk)