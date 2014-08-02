from django.db import models

from questapp.utils import trim


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Clue(BaseModel):
    show_num = models.SmallIntegerField(null=True, blank=True)
    game_id = models.SmallIntegerField(null=True, blank=True)
    question = models.CharField(max_length=255, null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return "G: {} S:{} C:{} Q:{} A:{}".format(
            self.game_id, self.show_num, self.category,
            trim(self.question), trim(self.answer))
