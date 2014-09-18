"""
Parses the samples html files and loads them to db.
"""
import logging
from questapp.utils import  read_local_html
from questapp.jeap_src_utils import SRC_GAME_IDS
from questapp.parser import parse_game_html
from questapp.models import Clue, Game
from django.core.management.base import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Parses the samples html files and loads them to db.'

    def handle(self, *args, **options):

        for game_id in SRC_GAME_IDS:
            html = read_local_html(game_id)
            if not html:
                continue
            parse_game_html(html, game_id)

        log.info("Loaded samples. {} games, {} clues.".format(
            Game.objects.count(), Clue.objects.count()))

