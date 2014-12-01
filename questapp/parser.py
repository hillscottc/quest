import re
import datetime
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game, Category
from django.db import DataError, transaction
from django.db import DatabaseError, IntegrityError
from .exceptions import MetadataParseException, CategoryException, HrefException
import logging

log = logging.getLogger(__name__)


class ParseErrors(Exception):
    """Takes a list of errors."""
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors


def parse_game_html(page, game_id):
    """Parse game and clues from html page, saves to db.
    """
    game, errors = None, []
    bs_game = BeautifulSoup(page)

    # Parse and upsert game metadata.
    game_meta = parse_game_meta(bs_game)

    try:
        game, created = Game.objects.get_or_create(sid=game_meta['show_num'],
                                                   gid=game_id,
                                                   title=game_meta['title'],
                                                   air_date=game_meta['air_date'],
                                                   comments=game_meta['comments'])
    except DatabaseError as err:
        mdp = MetadataParseException(err)
        log.error(mdp)
        return None, [mdp]

    # Parse and save the games's clues.
    try:
        _parse_game_clues(bs_game, game)
    except ParseErrors as pe:
        errors = pe.errors
    except Exception as err:
        log.exception("Failed parse clues for %s" % game)
        errors.append(err)

    # if len(game.clue_set.all()) == 0:
    #     errors.append(CluelessGameException())

    return game, errors


def parse_game_meta(bs_game):
    """Parse the show's metadata. """
    # Get the title
    if not bs_game.title:
        log.warn("No title section.")
        return

    title = bs_game.title.text

    comments = bs_game.find('div', {'id': 'game_comments'})
    if comments:
        comments = comments.text[:250]


    m = re.search(r'#(\d+)',title)
    show_num = m.group(1) if m else None

    m = re.search(r'(\d{4}-\d{2}-\d{2})', title)
    if not m:
        air_date = None
    else:
        air_date = datetime.datetime.strptime(m.group(1), '%Y-%m-%d')

    return dict(title=title, show_num=show_num, air_date=air_date,
                comments=comments)


def _parse_game_clues(bs_game, game):
    errors = []
    try:
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
    except CategoryException:
        log.exception("Failed cat parse of %s" % game)

    if errors:
        raise ParseErrors("Errors parsing game {}".format(game), errors)


def _parse_rounds(bs_game, game):
    clue_data_list = []
    for round_name in ['jeopardy_round', 'double_jeopardy_round']:
        round_div = bs_game.find('div', {'id': round_name})
        if not round_div:
            continue

        # Get the categories
        try:
            cats = _parse_round_cats(round_div, game)
        except CategoryException:
            raise

        for row in round_div.table.find_all('tr')[1:]:
            clues = row.find_all('td', {'class': "clue"})
            if not clues:
                continue
            for i, clue in enumerate(clues):
                if not clue.div:
                    continue

                category = cats[i]
                if not category:
                    continue

                # Get the q and a by parsing the messy div javascript
                question, answer = _parse_qa(clue.div)
                if not (question and answer):
                    continue

                question, answer = _parse_qa(clue.div)
                # yield dict(category=category, question=question, answer=answer)
                clue_data_list.append(dict(category=category, question=question, answer=answer))
    return clue_data_list


def _parse_round_cats(round_div, game):
    cats = []

    cat_row = round_div.table.find_all('tr')[0]
    if not cat_row:
        raise CategoryException("No cat row in game %s" % game)

    cat_els = cat_row.find_all('td', {'class': "category_name"})
    if not cat_els or len(cat_els) < 6:
        raise CategoryException("Expected 6 cat els in %s, got %s" % (game, len(cat_els)))

    for cat_el in cat_els:
        if not cat_el.text:
            # raise CategoryException("No category text in game %s" % game)
            log.warn("No category text in game %s" % game)
            cats.append(None)
        elif re.match('_+ *& *_+', cat_el.text):
            ## Catches bad '___& ___' categories.
            # raise CategoryException("Bad category in game %s, %s" % (game, cat_el.text))
            log.warn("Bad category in game %s, %s" % (game, cat_el.text))
            cats.append(None)
        else:
            cats.append(Category.objects.create(name=cat_el.text, game=game))

    if len(cats) is not 6:
        raise CategoryException("Expected 6 cats in %s, got %s" % (game, len(cats)))

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

