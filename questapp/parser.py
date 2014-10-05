import re
from string import split
from bs4 import BeautifulSoup
from .models import Clue, Game, Category
from django.db import DataError, transaction
from django.db import DatabaseError, IntegrityError
import logging


log = logging.getLogger(__name__)


class ParserErrors(Exception):
    """Takes a list of errors."""
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors


class HrefException(Exception):
    pass


class MetadataParseException(Exception):
    pass


class CategoryException(Exception):
    pass


def parse_game_html(page, game_id):
    """Parse game and clues from html page, saves to db.
    Returns db game and list of errors.
    """
    game, errors = None, []
    bs_game = BeautifulSoup(page)

    # Parse and upsert game metadata.
    game_meta = parse_game_meta(bs_game)
    if not game_meta.get('show_num'):
        mdp = MetadataParseException("Bad shum num.")
        return None, [mdp]

    try:
        game = Game.objects.get(sid=game_meta['show_num'])
    except Game.DoesNotExist:
        game = None

    if not game:
        try:
            game = Game.objects.create(sid=game_meta['show_num'], gid=game_id,
                                   title=game_meta['title'])
        except:
            game = None

    # Parse and save the games's clues.

    if game:
        try:
            _parse_rounds(bs_game, game)
        except ParserErrors as pe:
            errors = pe.errors
        except Exception as err:
            log.exception("Failed parse clues for %s" % game)
            errors.append(err)

    return game, errors


def parse_game_meta(bs_game):
    """Parse the show's metadata. """
    if not bs_game.title:
        log.warn("No title section.")
        return

    match_show_num = re.search(r'#(\d+)', bs_game.title.text)
    if not match_show_num:
        log.warn("No show number.")
        return

    return dict(show_num=match_show_num.group(1),
                title=bs_game.title)


def _parse_rounds(bs_game, game):
    for round_num, round_name in enumerate(['jeopardy_round', 'double_jeopardy_round']):
        round_div = bs_game.find('div', {'id': round_name})
        if not round_div:
            continue

        ## Parse cats for this round.
        _parse_round_cats(round_div, game, round_num)

        # cats = Category.objects.filter(game=game, round_num=round_num)


        for row in round_div.table.find_all('tr')[1:]:
            clues = row.find_all('td', {'class': "clue"})
            if not clues:
                continue
            for col_num, clue in enumerate(clues):
                if not clue.div:
                    continue

                try:
                    cat = Category.objects.get(game=game, col_num=col_num, round_num=round_num)
                except Category.DoesNotExist:
                    continue
                except Exception:
                    log.warn('prob with category.')

                    # import pdb
                    # pdb.set_trace()

                    continue

                try:
                    _parse_qa(clue.div, cat)
                except:
                    log.exception("Error parsing round.")
                    continue


def _parse_round_cats(round_div, game, round_num):
    cat_row = round_div.table.find_all('tr')[0]

    for col_num, cat_el in enumerate(cat_row.find_all('td', {'class': "category_name"})):
        cat_name = None
        if not cat_el.text:
            log.warn("No category text in game %s" % game)
        elif cat_el.text == '_______ & _______':
            log.warn("Bad category in game %s, %s" % (game, cat_el.text))
        else:
            cat_name = cat_el.text

        try:
            existing_cat = Category.objects.get(game=game, name=cat_name, col_num=col_num, round_num=round_num)
        except:
            existing_cat = None

        if not existing_cat:
            try:
                Category.objects.create(game=game, name=cat_name, col_num=col_num, round_num=round_num)
            except:
                pass


def _parse_qa(div_tag, cat):
    """Gets raw text by parsing q and a from div's mouseover js."""
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

    if not cat or not question or not answer:
        return
    elif len(question) > 255 or len(answer) > 255:
        return
    elif len(question) < 3:
        return
    elif '<a href' in question:
        # errors.append(HrefException(clue_data['question']))
        return

    try:
        existing = Clue.objects.get(category=cat,  question=question, answer=answer)
    except Clue.DoesNotExist:
        existing = None

    try:
        if not existing:
            Clue.objects.create(category=cat,  question=question, answer=answer)
    except:
        log.warn("Error creating clue.")
        return

