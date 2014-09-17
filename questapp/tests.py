import os
from unittest import skipUnless
from django.test.utils import override_settings
from questapp.management.commands import load_samples
from .models import Clue, Game, Category
from .parser import parse_game_html
from .utils import (TEST_GAME_ID, TEST_SHOW_NUM,
                    get_sample_ids, read_local_html,
                    get_fname, get_random_objs)
from django.test import TestCase
# from django_nose import FastFixtureTestCase as TestCase
# REUSE_DB = 1

TEST_WITH_FIXTURES = True


class FuntionalTest(TestCase):

    if TEST_WITH_FIXTURES:
        fixtures = ['samples.json']

    def setUp(self):
        print

    @skipUnless(TEST_WITH_FIXTURES, "Check the loaded test fixtures.")
    def test_loaded_fixtures(self):
        """Check the loaded test fixtures."""
        print "Game count:", Game.objects.count()
        self.assertGreater(Game.objects.count(), 100)
        self.assertGreater(Clue.objects.count(), 7000)
        num_cats = len(set([clue.category for clue in Clue.objects.all()]))
        print "Categories  :", num_cats
        self.assertGreater(num_cats, 900)

    @skipUnless(not TEST_WITH_FIXTURES, "Parse and load all html sample files.")
    def test_load_samples(self):
        """Execute the load_samples mgmt command, loading the db."""
        print
        load_samples.Command().handle()

        game_count = Game.objects.count()
        print "Count Games:", game_count
        self.assertEqual(game_count,
                         len(list(get_sample_ids())) - 1)

        clue_count = Clue.objects.count()
        print "Count Clues:", clue_count
        self.assertGreater(clue_count, 9900)  # 9913

        cat_count = Category.objects.count()
        print "Count Categories:", cat_count
        self.assertGreater(cat_count, 2300)  # 2358

    def test_get_random_objs(self):
        """Get a random Clue and Category."""
        if not Clue.objects.count():
            print "No Clues."
            return

        print "Some random clues."
        clue1 = get_random_objs(Clue).next()
        print clue1.desc()
        self.assertIsNotNone(clue1)
        clue2 = get_random_objs(Clue).next()
        print clue2.desc()
        self.assertIsNotNone(clue2)
        self.assertNotEqual(clue1.pk, clue2.pk)

        print "Some random categories."
        for cat in get_random_objs(Category, 5):
            print cat


class UnitTest(TestCase):
    def test_get_sample_ids(self):
        """Get list of game_ids from samples."""
        game_ids = list(get_sample_ids())
        self.assertGreater(len(game_ids), 10)

    def test_read_local(self):
        """Open local test game file."""
        html = read_local_html(TEST_GAME_ID)
        length = len(html) if html else 0
        self.assertGreater(length, 3000)

    def test_get_fname(self):
        """Create file name for given id."""
        fname = get_fname(TEST_GAME_ID)
        self.assertIsNotNone(fname)
        self.assertTrue(os.path.isfile(fname))

    @override_settings(DEBUG=True)
    def test_parse_game(self):
        """Parse the test game, save to db.
        Debug settings overrided.
        """
        html = read_local_html(TEST_GAME_ID)
        game = parse_game_html(html, TEST_GAME_ID)

        print game

        self.assertEqual(game.game_id, TEST_GAME_ID)
        self.assertEqual(game.show_num, TEST_SHOW_NUM)

        clues = game.clue_set.all()
        self.assertEqual(len(clues), 48)
        print "First five clues in game {}:".format(TEST_GAME_ID)
        for clue in game.clue_set.all()[:5]:
            print clue,
        print

    def test_upsert(self):
        """Test game upserts."""
        html = read_local_html(TEST_GAME_ID)
        test_game = parse_game_html(html, TEST_GAME_ID)
        self.assertEqual(test_game.game_id, TEST_GAME_ID)
        self.assertEqual(test_game.show_num, TEST_SHOW_NUM)

        fake_game_id = 8888
        fake_show_num = 9999

        # update it by calling upsert with same num
        game, created = Game.objects.upsert(show_num=test_game.show_num,
                                            defaults=dict(game_id=fake_game_id))
        self.assertEqual(game.game_id, fake_game_id)
        self.assertEqual(game.show_num, TEST_SHOW_NUM)
        self.assertFalse(created)

        # create a game by upsert new num
        game, created = Game.objects.upsert(show_num=fake_show_num,
                                            defaults=dict(game_id=fake_game_id))
        self.assertEqual(game.game_id, fake_game_id)
        self.assertEqual(game.show_num, fake_show_num)
        self.assertTrue(created)


