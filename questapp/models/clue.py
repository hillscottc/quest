import logging
from django.db import models
from django.core.urlresolvers import reverse
from .common import BaseModel

log = logging.getLogger(__name__)


class Clue(BaseModel):
    category = models.CharField(max_length=255)
    question = models.CharField(max_length=355)
    answer = models.CharField(max_length=355)

    class Meta:
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




