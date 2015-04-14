from django.test import TestCase
from unittest import skip
from django.db.models import Count
from questapp.utils import load_clues
from questapp.utils import dbstore_get
import datetime as dt
from questapp.models import UserLog, CountCase, Clue, DbStore
from questproj.views import get_counts
from django.contrib.auth.models import User


class LogTest(TestCase):

    def setUp(self):
        obj = UserLog.objects.create(userid=0, questionid=91, correct=False)
        obj.created = dt.datetime.now() - dt.timedelta(hours=48)
        obj.save()
        UserLog.objects.create(userid=0, questionid=91, correct=False)
        UserLog.objects.create(userid=0, questionid=91, correct=False)
        UserLog.objects.create(userid=0, questionid=91, correct=True)
        UserLog.objects.create(userid=0, questionid=92, correct=False)
        UserLog.objects.create(userid=0, questionid=92, correct=True)
        UserLog.objects.create(userid=1, questionid=91, correct=False)
        obj = UserLog.objects.create(userid=1, questionid=91, correct=False)
        obj.created = dt.datetime.now() - dt.timedelta(hours=48)
        obj.save()
        UserLog.objects.create(userid=1, questionid=91, correct=False)
        UserLog.objects.create(userid=1, questionid=91, correct=True)
        UserLog.objects.create(userid=1, questionid=92, correct=False)
        print
        print "All rows:"
        for row in UserLog.objects.all():
            print row
        print
        # user = User.objects.create(username='shill')

    def test_get_daily_counts(self):
        rows = UserLog.get_daily_counts()
        print "Counts by day user."
        for row in rows:
            print row
        self.assertEquals(len(rows), 4)

    def test_get_counts_by_date(self):
        rows = UserLog.get_counts_by_date(dt.date.today())
        print "Today's rows:"
        for row in rows:
            print row
        self.assertEquals(len(rows), 2)


class UnitTest(TestCase):

    def test_dbstore(self):
        test_key = "color"
        test_val = "blue"
        DbStore.objects.create(dbkey=test_key, dbval=test_val)
        result = dbstore_get(test_key, None)
        print "Got ", result
        self.assertEqual(test_val, result)


@skip("Skipping load test.")
class TestLoad(TestCase):
    def test_load_clues(self):
        """Load clues json file.
        """
        infile = 'questproj/fixtures/clues.json'
        load_clues(infile)
        count = Clue.objects.count()
        self.assertGreater(count, 5)





