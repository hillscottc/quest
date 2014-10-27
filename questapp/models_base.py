import logging
from django.db import models
from django.contrib.auth.models import User


log = logging.getLogger(__name__)


class BaseModelManager(models.Manager):

    def update(self, **kwargs):
        fieldnames = [field.name for field in self._meta.fields]
        for attr, value in kwargs.iteritems():
            if attr in fieldnames and hasattr(self, attr):
                setattr(self, attr, value)
        self.save()


    # def upsert(self, **kwargs):
    #     """Insert or update.
    #     Usage: x.upsert(name='joe', defaults=dict(id=1))
    #     """
    #     obj, created = self.get_or_create(**kwargs)
    #     if not created and "defaults" in kwargs:
    #         for k, v in kwargs.get("defaults", {}).items():
    #             if k not in dir(obj):
    #                 raise AttributeError(
    #                     "Bad attr {} for update on {} ({})".format(
    #                         k, type(obj), obj.pk))
    #             setattr(obj, k, v)
    #         obj.save()
    #
    #     if created:
    #         log.debug("Created {}.".format(obj))
    #     else:
    #         log.debug("Updated {}.".format(obj))
    #
    #     return obj, created


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, editable=False)
    last_accessed = models.DateTimeField(auto_now=True, editable=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True
        ordering = ["-modified"]



