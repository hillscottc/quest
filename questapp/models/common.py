import logging
from datetime import datetime, date
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

    objects = BaseModelManager()

    class Meta:
        abstract = True
        ordering = ["-created"]


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    modified = models.DateTimeField(auto_now=True, editable=False, default=datetime.now)

    def __unicode__(self):
        return self.user.username


class UserLog(models.Model):
    """Trying not to use foreign keys in a log class.
    """
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    userid = models.IntegerField(default=0)
    questionid = models.IntegerField(default=0)
    correct = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('userlog-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{}, {}, {}".format(self.created, self.userid, self.questionid)

    @staticmethod
    def get_counts(user):
        counts = {}
        if user.username:
            counts['user_today_right'] = UserLog.objects.filter(
                created__gte=date.today(),
                correct=True,
                userid=user.id).count()
            counts['user_today_wrong'] = UserLog.objects.filter(
                created__gte=date.today(),
                correct=False,
                userid=user.id).count()
            counts['user_alltime_right'] = UserLog.objects.filter(
                correct=True,
                userid=user.id).count()
            counts['user_alltime_wrong'] = UserLog.objects.filter(
                correct=False,
                userid=user.id).count()
        else:
            counts['user_today_right'] = '-'
            counts['user_today_wrong'] = '-'
            counts['user_alltime_right'] = '-'
            counts['user_alltime_wrong'] = '-'

        counts['everyone_today_right'] = UserLog.objects.filter(
            correct=True,
            created__gte=date.today()).count()
        counts['everyone_today_wrong'] = UserLog.objects.filter(
            correct=False,
            created__gte=date.today()).count()
        counts['everyone_alltime_right'] = UserLog.objects.filter(correct=True).count()
        counts['everyone_alltime_wrong'] = UserLog.objects.filter(correct=False).count()
        return counts


class DbStore(models.Model):
    dbkey = models.CharField(max_length=255)
    dbval = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{} : {}".format(self.dbkey, self.dbval)
