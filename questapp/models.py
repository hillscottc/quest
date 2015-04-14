import logging
from datetime import datetime
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


# Two util classes to get aggregate count with case https://djangosnippets.org/snippets/2100/

class SQLCountCase(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'COUNT'
    sql_template = "%(function)s(CASE %(case)s WHEN %(when)s THEN 1 ELSE null END)"

    def __init__(self, col, **extra):
        if isinstance(extra['when'], basestring):
            extra['when'] = "'%s'"%extra['when']

        if not extra.get('case', None):
            extra['case'] = '"%s"."%s"'%(extra['source'].model._meta.db_table, extra['source'].name)

        if extra['when'] is None:
            extra['when'] = True
            extra['case'] += ' IS NULL '

        super(SQLCountCase, self).__init__(col, **extra)


class CountCase(models.Aggregate):
    name = 'COUNT'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLCountCase(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate


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
        return u"{}, {}, {}".format(self.created.strftime("%Y-%m-%d %H:%M"), self.userid, self.questionid)


class DbStore(models.Model):
    dbkey = models.CharField(max_length=255)
    dbval = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{} : {}".format(self.dbkey, self.dbval)


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

    @staticmethod
    def get_random_cats(num=20):
        """Get random list of categories."""
        cats = [c.category for c in Clue.objects.all().order_by('?')[:num]]
        return cats

    def __unicode__(self):
        return u"Q:{} A:{}".format(self.question, self.answer)
