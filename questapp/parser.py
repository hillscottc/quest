import re
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game
from django.db import DataError, transaction
from django.db.transaction import TransactionManagementError

ROUNDS_PARSED = ['jeopardy_round', 'double_jeopardy_round']


def parse_game_html(page, game_id=None):
    """
    Parse clues from html page.
    """
    bs = BeautifulSoup(page)
    show_num = None
    if bs.title:
        match = re.search(r'#(\d+)', bs.title.text)
        show_num = match.group(1) if match else None

    game = Game(game_id=game_id, show_num=show_num)

    game_rounds = []
    for round_name in ROUNDS_PARSED:
        game_round = _parse_round(round_div=bs.find('div', {'id': round_name}))
        game_rounds.append(game_round)

    for game_round in game_rounds:
        for clue in game_round:
            # yield clue
            try:
                with transaction.atomic():
                    game.clue_set.add(clue)
            except (DataError, TransactionManagementError):
                # print "Failed", model_to_dict(clue)
                print "Failed a clue"

    return game


def _parse_round(round_div):
    """
    Parse clues from a round div.
    """
    if not round_div:
        return

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




