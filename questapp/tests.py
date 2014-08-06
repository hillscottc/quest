import os
from django.test import TestCase
from django.forms.models import model_to_dict

from .models import Clue, Game
from .game_mgr import GameMgr, TEST_GAME_ID, load_all_games

mgr = GameMgr()


class SamplesTest(TestCase):
    def setUp(self):
        print

    def test_load_all_games(self):
        """
        Test loading all samples into db.
        """
        parsed, failed = load_all_games()
        "Games parsed:", len(parsed), ", failed:", len(failed)


        games = Game.objects.all()



        print "Loaded games to db:", len(games)
        self.assertGreater(len(games), 100)

        clues = Clue.objects.all()
        print "Loaded clues to db:", len(clues)
        self.assertGreater(len(clues), 7000)

        num_cats = len(set([clue.category for clue in clues]))
        print "Categories  :", num_cats
        self.assertGreater(num_cats, 900)


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
        game = list(mgr.parse_games(TEST_GAME_ID))[0]
        game.save()
        print
        count = Clue.objects.count()
        self.assertEqual(count, 50)
        for clue in Clue.objects.all()[:5]:
            print clue

