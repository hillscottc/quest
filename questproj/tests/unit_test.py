import os
from django.test import TestCase
from unittest import skip
from django.db.models import Count
from questapp.utils import load_clues
from questapp.utils import dbstore_get
import datetime as dt
from questapp.models import UserLog, Clue, DbStore
from postmark import PMMail

def print_counts(rows):
    print "{:<10} {} {} {} {}".format('day', 'userid', 'is_correct_yes', 'total', 'percentage')
    for row in rows:
        print "{} {:<6} {:<14} {:<5} {}".format(
            row['day'], row['userid'], row['is_correct_yes'], row['total'], row['percentage'])


class USerLogTest(TestCase):

    def setUp(self):
        print
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

        print "All rows:"
        for row in UserLog.objects.all():
            print row
        print
        # user = User.objects.create(username='shill')

    def test_counts_filtered(self):

        rows = UserLog.get_counts_filtered()
        print_counts(rows)
        self.assertEquals(len(rows), 11)

        print

        rows = UserLog.get_counts_filtered(count_filter=None,
                                           group_by=('day', ))
        print "{:<10} {} {} {}".format('day', 'is_correct_yes', 'total', 'percentage')
        for row in rows:
            print "{} {:<14} {:<5} {}".format(
                row['day'], row['is_correct_yes'], row['total'], row['percentage'])
        self.assertEquals(len(rows), 2)

        print

        rows = UserLog.get_counts_filtered(count_filter={'created__gte': dt.date.today()},
                                           group_by=('day', 'userid'))
        print_counts(rows)
        self.assertEquals(len(rows), 2)

        print

        rows = UserLog.get_counts_filtered(count_filter={'userid': 1},
                                           group_by=('day', 'userid'))
        print_counts(rows)
        self.assertEquals(len(rows), 2)

        print

        rows = UserLog.get_counts_filtered(count_filter={'userid': 1, 'created__gte': dt.date.today()},
                                           group_by=('day', 'userid'))
        print_counts(rows)
        self.assertEquals(len(rows), 1)


class UnitTest(TestCase):

    def test_dbstore(self):
        test_key = "color"
        test_val = "blue"
        DbStore.objects.create(dbkey=test_key, dbval=test_val)
        result = dbstore_get(test_key, None)
        print "Got ", result
        self.assertEqual(test_val, result)


# @skip("Skipping postmark email test.")
class UnitTest(TestCase):

    def test_postmark_email(self):
        message = PMMail(api_key=os.environ.get('POSTMARK_API_TOKEN'),
                         subject="Testing from Postmark",
                         sender="scott@trivquest.com",
                         to="scott289@gmail.com",
                         text_body="Testing",
                         tag="test")
        message.send()


@skip("Skipping load test.")
class TestLoad(TestCase):
    def test_load_clues(self):
        """Load clues json file.
        """
        infile = 'questproj/fixtures/clues.json'
        load_clues(infile)
        count = Clue.objects.count()
        self.assertGreater(count, 5)





