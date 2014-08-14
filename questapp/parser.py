import re
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game
from django.db import DataError, transaction
from django.db import DatabaseError
import logging

log = logging.getLogger(__name__)


def parse_game_html(page, game_id):
    """Parse game and clues from html page, saves to db.
    """
    bs_game = BeautifulSoup(page)

    # Get the title
    if not bs_game.title:
        log.warn("No title section.")
        return

    # Get the show num
    match_show_num = re.search(r'#(\d+)', bs_game.title.text)
    if not match_show_num:
        log.warn("No show number.")
        return
    show_num = int(float(match_show_num.group(1)))

    # Create/update game.
    try:
        game, created = Game.objects.upsert(show_num=show_num,
                                            defaults=dict(game_id=game_id))
    except DatabaseError as err:
        log.warn(err)
        return

    # Delete old clues.
    if not created:
        [clue.delete() for clue in game.clue_set.all()]

    for clue in list(parse_clues(bs_game)):
        with transaction.atomic():
            try:
                clue, created = Clue.objects.upsert(game=game,
                                                    category=clue.category,
                                                    question=clue.question,
                                                    answer=clue.answer)
            except DataError as err:
                log.warn(("Failed parse of clue "
                          "{}, {}, {}".format(game_id, clue, err)))
    return game


def parse_clues(bs_game):
    """Yields Clues parsed from given souped game.
    """
    for round_name in ['jeopardy_round', 'double_jeopardy_round']:
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
