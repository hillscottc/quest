import os
from django.test import TestCase

from .models import Clue
from .game_mgr import GameMgr, TEST_GAME_ID

mgr = GameMgr()


class SamplesTest(TestCase):
    def setUp(self):
        """
        Parse and save all sample games to db.
        """
        clues = mgr.parse_games(*mgr.get_sample_ids())
        for clue in clues:
            clue.save()
        print

    def test_db(self):
        """
        Test samples loaded into db.
        """
        clues = Clue.objects.all()
        print "Loaded clues to db:", Clue.objects.count()
        self.assertGreater(len(clues), 7000)

        num_cats = len(set([clue.category for clue in clues]))
        print "Categories  :", num_cats
        self.assertGreater(num_cats, 900)

        num_show_nums = len(set([clue.show_num for clue in clues]))
        print "Show Nums  :", num_show_nums
        self.assertGreater(num_show_nums, 100)

        num_game_ids = len(set([clue.game_id for clue in clues]))
        print "Game ids  :", num_game_ids
        self.assertGreater(num_game_ids, 100)


class UnitTest(TestCase):

    def test_get_sample_ids(self):
        """
        Able to get list of game_ids from samples?
        """
        game_ids = list(mgr.get_sample_ids())
        self.assertGreater(len(game_ids), 10)

    def test_get_local(self):
        """
        Test opening local game files.
        """
        html = mgr.get_local_html(TEST_GAME_ID)
        length = len(html) if html else 0
        self.assertGreater(length, 3000)

    def test_get_fname(self):
        """
        Create file name for given id.
        """
        fname = mgr.get_fname(TEST_GAME_ID)
        self.assertIsNotNone(fname)
        self.assertTrue(os.path.isfile(fname))

    def test_save_clues(self):
        """
        Test db read and write of clues.
        """
        clues = mgr.parse_games(TEST_GAME_ID)
        for clue in clues:
            clue.save()

        count = Clue.objects.count()
        self.assertEqual(count, 50)
        for clue in Clue.objects.all()[:5]:
            print clue

