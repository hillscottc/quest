from django.db import models
from questapp.utils import trim


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Game(BaseModel):
    show_num = models.SmallIntegerField(default=0)
    game_id = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return "{}/{}".format(self.game_id, self.show_num)


class Clue(BaseModel):
    game = models.ForeignKey(Game, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    def __unicode__(self):
        return " C:{} Q:{} A:{}".format(self.category, trim(self.question), trim(self.answer))
