import re
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game, Category
from django.db import DataError, transaction
from django.db import DatabaseError
import logging

log = logging.getLogger(__name__)


def parse_game_html(page, game_id):
    """Parse game and clues from html page, saves to db.
    """
    bs_game = BeautifulSoup(page)

    # Parse and upsert game metadata.
    game_meta = parse_game_meta(bs_game)
    try:
        game, created = Game.objects.upsert(show_num=game_meta['show_num'],
                                            defaults=dict(game_id=game_id))
    except DatabaseError as err:
        log.warn(err)
        return

    # Delete any old clues or cats for this game.
    if not created:
        [clue.delete() for clue in game.clue_set.all()]
        [cat.delete() for cat in game.category_set.all()]

    # Parse and save the games's clues.
    _parse_game_clues(bs_game, game)

    return game


def parse_game_meta(bs_game):
    """Parse the show's metadata. """
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

    return dict(show_num=show_num)


def _parse_game_clues(bs_game, game):
    for clue_data in _parse_rounds(bs_game, game):
        if len(clue_data['question']) < 3:
            continue

        if '<a href' in clue_data['question']:
            log.debug("Skipping a question containing an href.")
            continue

        with transaction.atomic():
            try:
                Clue.objects.create(game=game, category=clue_data['category'],
                                    question=clue_data['question'],
                                    answer=clue_data['answer'])
            except DataError as err:
                log.warn(("Failed parse clue_data {}, {}".format(clue_data, err)))


def _parse_rounds(bs_game, game):
    for round_name in ['jeopardy_round', 'double_jeopardy_round']:
        round_div = bs_game.find('div', {'id': round_name})
        if not round_div:
            continue

        # Get the categories
        cats = _parse_round_cats(round_div, game)

        for row in round_div.table.find_all('tr')[1:]:
            clues = row.find_all('td', {'class': "clue"})
            if not clues:
                continue
            for i, clue in enumerate(clues):
                if not clue.div:
                    continue
                # Get the q and a by parsing the messy div javascript
                question, answer = _parse_qa(clue.div)
                if not (question and answer):
                    continue

                question, answer = _parse_qa(clue.div)
                yield dict(category=cats[i], question=question, answer=answer)


def _parse_round_cats(round_div, game):
    cat_row = round_div.table.find_all('tr')[0]
    cats = []
    for cat_el in cat_row.find_all('td', {'class': "category_name"}):
        # cat, _ = Category.objects.upsert(defaults=dict(name=cat_el.text, game=game))
        cats.append(Category.objects.create(name=cat_el.text, game=game))
    return cats


def _parse_qa(div_tag):
    """Parse the q and a from div's mouseover js."""
    question, answer = '', ''
    regex_ans = '(.*)("correct_response">)([^<]+)'

    raw_answer = div_tag.get('onmouseover')
    raw_question = div_tag.get('onmouseout')

    if raw_answer and raw_question:
        question = split(raw_question, ", '",  2)[2][:-2]





        match = re.match(regex_ans, raw_answer)
        answer = match.group(3) if match else ''

    # Remove backslashes -- shouldn't be any escaping in the source.
    question = re.sub(r"\\", "", question)
    answer = re.sub(r"\\", "", answer)

    return question, answer
