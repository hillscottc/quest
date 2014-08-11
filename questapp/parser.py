import re
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game
from django.db import DataError, transaction
from django.db import DatabaseError, IntegrityError
import logging
# from django.db.transaction import TransactionManagementError

log = logging.getLogger(__name__)


def parse_game_html(page, game_id=None):
    """Parse clues from html page.
    """
    bs_game = BeautifulSoup(page)

    if not bs_game.title:
        log.warn("No title section.")
        return

    match_show_num = re.search(r'#(\d+)', bs_game.title.text)
    if not match_show_num:
        log.warn("No show number.")
        return

    game = None
    try:
        game, created = Game.objects.upsert(show_num=match_show_num.group(1),
                                            **dict(game_id=game_id))
        if created:
            log.info("Created game {}.".format(game))
        else:
            log.info("Updated game {}.".format(game))
    except DatabaseError as err:
        log.warn(err)

    if game:
        for clue in list(parse_clues(bs_game)):
            with transaction.atomic():
                try:
                    game.clue_set.add(clue)
                except DataError as err:
                    log.warn(("Failed parse of clue"
                              "{}, {}, {}".format(game_id, clue, err)))
    return game


def parse_clues(bs_game):

    for round_name in ['jeopardy_round', 'double_jeopardy_round']:
        # game_round = _parse_round(round_div=bs.find('div', {'id': round_name}))
        round_div = bs_game.find('div', {'id': round_name})
        if not round_div:
            continue
        jrt = round_div.table

        cat_tags = jrt.find_all('tr')[0].find_all('td', {'class': "category_name"})
        cats = [t.text for t in cat_tags]

        for row in jrt.find_all('tr')[1:]:
            clues = row.find_all('td', {'class': "clue"})
            if not clues:
                continue
            for i, clue in enumerate(clues):
                if not clue.div:
                    continue
                else:
                    question, answer = _parse_clue(clue.div)
                    yield Clue(category=cats[i], question=question, answer=answer)


def _parse_clue(div_tag):
    """Parse the q and a from div's mouseover js."""
    question, answer = '', ''
    regex_ans = '(.*)("correct_response">)([^<]+)'

    raw_answer = div_tag.get('onmouseover')
    raw_question = div_tag.get('onmouseout')

    if raw_answer and raw_question:
        question = split(raw_question, ", '",  2)[2][:-2]
        match = re.match(regex_ans, raw_answer)
        answer = match.group(3) if match else ''

    return question, answer



