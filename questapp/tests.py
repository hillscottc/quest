import os
from django.test import TestCase

from questapp.models import Clue
from questapp.game_mgr import (get_fname, get_local_html,
                               parse_game_ids, GAME_IDS)


TEST_GAME_ID = 4529


class SamplesTest(TestCase):
    def setUp(self):
        """
        Parse and save sample games to db.
        """
        clues = parse_game_ids(*GAME_IDS)
        for clue in clues:
            clue.save()
        print "Loaded clues to db:", Clue.objects.count()

    def test_clues(self):
        clues = Clue.objects.all()
        self.assertGreater(len(clues), 7000)

        num_cats = len(set([clue.category for clue in clues]))
        print "Categories  :", num_cats
        self.assertGreater(num_cats, 900)


class UnitTest(TestCase):

    def test_get_local(self):
        """Test opening local game files."""
        html = get_local_html(TEST_GAME_ID)
        length = len(html) if html else 0
        print "Game id", TEST_GAME_ID, "length", length
        self.assertGreater(length, 3000)

    def test_get_fname(self):
        """Create file name for given id."""
        fname = get_fname(TEST_GAME_ID)
        self.assertIsNotNone(fname)
        self.assertTrue(os.path.isfile(fname))

    def test_save_clues(self):
        """Test db read and write of clues."""
        print "Parse test game, write clues to db."
        clues = parse_game_ids(TEST_GAME_ID)
        for clue in clues:
            clue.save()

        print "Verify count of test game records."
        count = Clue.objects.count()
        self.assertEqual(count, 50)

