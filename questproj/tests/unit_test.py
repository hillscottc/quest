import os
from django.test import TestCase
from unittest import skip
from questapp.utils import load_clues
from questapp.utils import dbstore_get
import datetime as dt
from questapp.models import UserLog, Clue, DbStore
from postmark import PMMail
from django.conf import settings


class UserLogTest(TestCase):

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

    @staticmethod
    def print_counts(rows):
        print "\nday        userid is_correct_yes total percentage"
        for row in rows:
            print "{day} {userid:<6} {is_correct_yes:<14} {total:<5} {percentage}".format(**row)

    def test_counts_filtered(self):

        rows = UserLog.get_counts_filtered()
        # print_counts(rows)
        self.assertEquals(len(rows), 11)

        rows = UserLog.get_counts_filtered(count_filter=None, group_by=('day', ))
        print "\nday        is_correct_yes total percentage"
        for row in rows:
            print "{day} {is_correct_yes:<14} {total:<5} {percentage}".format(**row)
        self.assertEquals(len(rows), 2)

        rows = UserLog.get_counts_filtered(count_filter={'created__gte': dt.date.today()},
                                           group_by=('day', 'userid'))
        self.print_counts(rows)
        self.assertEquals(len(rows), 2)

        rows = UserLog.get_counts_filtered(count_filter={'userid': 1}, group_by=('day', 'userid'))
        self.print_counts(rows)
        self.assertEquals(len(rows), 2)

        rows = UserLog.get_counts_filtered(count_filter={'userid': 1, 'created__gte': dt.date.today()},
                                           group_by=('day', 'userid'))
        self.print_counts(rows)
        self.assertEquals(len(rows), 1)


class UnitTest(TestCase):

    def test_dbstore(self):
        test_key = "color"
        test_val = "blue"
        DbStore.objects.create(dbkey=test_key, dbval=test_val)
        result = dbstore_get(test_key, None)
        print "\nGot ", result
        self.assertEqual(test_val, result)


@skip("Skipping email test.")
class TestEmail(TestCase):

    def test_postmark_email(self):

        message = PMMail(api_key=os.environ.get('POSTMARK_API_TOKEN'),
                         subject="Testing PMMail",
                         sender=settings.POSTMARK_SENDER,
                         to="scott289@gmail.com",
                         text_body="testing", tag="test")
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





