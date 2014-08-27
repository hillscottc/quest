"""
Parses the samples html files and loads them to db.
"""
import logging
from questapp.utils import get_sample_ids, read_local_html
from questapp.parser import parse_game_html
from questapp.models import Clue, Game
from django.core.management.base import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Parses the samples html files and loads them to db.'

    def handle(self, *args, **options):

        for game_id in get_sample_ids():
            html = read_local_html(game_id)
            if not html:
                continue
            parse_game_html(html, game_id)

        log.info("Loaded samples. {} games, {} clues.".format(
            Game.objects.count(), Clue.objects.count()))

