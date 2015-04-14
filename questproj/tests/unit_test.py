from django.test import TestCase
from unittest import skip
from django.db.models import Count
from questapp.utils import load_clues
from questapp.utils import dbstore_get
from datetime import date
from questapp.models import UserLog, CountCase, Clue, DbStore
from questproj.views import get_counts
from django.contrib.auth.models import User


class TestLog(TestCase):

    def setUp(self):
        UserLog.objects.create(userid=0, questionid=91, correct=False)
        UserLog.objects.create(userid=0, questionid=91, correct=False)
        UserLog.objects.create(userid=0, questionid=91, correct=False)
        UserLog.objects.create(userid=0, questionid=91, correct=True)
        UserLog.objects.create(userid=0, questionid=92, correct=False)
        UserLog.objects.create(userid=0, questionid=92, correct=True)
        UserLog.objects.create(userid=1, questionid=91, correct=False)
        UserLog.objects.create(userid=1, questionid=91, correct=False)
        UserLog.objects.create(userid=1, questionid=91, correct=True)
        UserLog.objects.create(userid=1, questionid=92, correct=False)

    def test_counts(self):

        # user = User.objects.create(username='shill')
        # counts = get_counts(user)
        # print counts

        rows = UserLog.objects.filter(created__gte=date.today()).annotate(
            is_correct_yes=CountCase('correct', when=True),
            is_correct_no=CountCase('correct', when=False))

        print rows


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





