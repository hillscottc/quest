import re
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game, Category
from django.db import DataError, transaction
from django.db import DatabaseError, IntegrityError
import logging

log = logging.getLogger(__name__)


class ParseErrors(Exception):
    """Takes a list of errors."""
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors


class HrefException(Exception):
    pass


class MetadataParseException(Exception):
    pass


class CluelessGameException(Exception):
    pass


def parse_game_html(page, game_id):
    """Parse game and clues from html page, saves to db.
    """
    game, errors = None, []
    bs_game = BeautifulSoup(page)

    # Parse and upsert game metadata.
    game_meta = parse_game_meta(bs_game)
    try:
        game, created = Game.objects.upsert(show_num=game_meta['show_num'],
                                            defaults=dict(game_id=game_id))
    except DatabaseError as err:
        print err
        raise MetadataParseException(err)

    # Delete any old clues or cats for this game.
    if not created:
        [clue.delete() for clue in game.clue_set.all()]
        [cat.delete() for cat in game.category_set.all()]

    # Parse and save the games's clues.
    try:
        _parse_game_clues(bs_game, game)
    except ParseErrors as pe:
        errors = pe.errors

    # if len(game.clue_set.all()) == 0:
    #     errors.append(CluelessGameException())

    return game, errors


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

    errors = []

    for clue_data in _parse_rounds(bs_game, game):
        if len(clue_data['question']) < 3:
            continue

        if '<a href' in clue_data['question']:
            errors.append(HrefException(clue_data['question']))
            # log.debug("Skipping a question containing an href.")
            continue

        with transaction.atomic():
            try:
                Clue.objects.create(game=game, category=clue_data['category'],
                                    question=clue_data['question'],
                                    answer=clue_data['answer'])
            except (IntegrityError, DataError) as err:
                errors.append(err)
                # log.warn(("Failed parse clue_data {}, {}".format(clue_data, err)))
    if errors:
        raise ParseErrors("Errors parsing game {}".format(game), errors)


def _parse_rounds(bs_game, game):
    for round_name in ['jeopardy_round', 'double_jeopardy_round']:
        round_div = bs_game.find('div', {'id': round_name})
        if not round_div:
            continue

        # Get the categories
        try:
            cats = _parse_round_cats(round_div, game)
        except (IntegrityError, DataError):
            ## Just log it for now, and try next round
            log.exception("Err getting round cats for %s" % game)
            continue

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

    # Removing these corrects the backslash-escaped-quotes.
    question = re.sub(r"\\", "", question)
    answer = re.sub(r"\\", "", answer)

    return question, answer
