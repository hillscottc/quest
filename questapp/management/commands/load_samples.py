"""
Parses the samples html files and loads them to db.
"""
from questapp.game_mgr import load_all_games
from questapp.models import Clue, Game
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Parses the samples html files and loads them to db.'

    def handle(self, *args, **options):
        load_all_games()
        self.stdout.write("Loaded samples. {} games, {} clues.".format(
            Game.objects.count(), Clue.objects.count()))

