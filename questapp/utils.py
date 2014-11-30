import os
import logging
import re
from bs4 import BeautifulSoup
import requests
from django.conf import settings
from questapp.parser import parse_game_html

log = logging.getLogger(__name__)

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='
TEST_GAME_ID = 4529
TEST_SHOW_NUM = 153


def get_fname(game_id):
    """Returns valid sampledir filename for given id.
    """
    if isinstance(game_id, int):
        game_id = str(game_id)
    return os.path.join(settings.JEAP_SRC_DIR, "game_{}.html".format(game_id))


def write_game(game_id, html):
    """Save html as a file in the SAMPLE_DIR, named with the id.
    """
    if len(html) < 3000:
        return

    fname = get_fname(game_id)
    try:
        with open(fname, "w") as outfile:
            outfile.write(html.encode('utf-8'))
        return fname
    except UnicodeEncodeError as uni_err:
        log.warn("Unicode error writing game {}, {}".format(fname, uni_err))
        return None


def get_remote_html(game_id):
    """Makes http request to host, returns html text.
    """
    game_id = str(game_id) if isinstance(game_id, int) else game_id
    url = URL_BASE + game_id
    return requests.get(url).text


def save_remote_games(*game_ids):
    """Gets remote games and saves them to db. See SRC_GAME_IDS for a list.
    """
    for game_id in game_ids:
        html = get_remote_html(game_id)
        write_game(game_id, html)


def read_local_html(game_id):
    """Reads and returns local game file text.
    """
    game_id = str(game_id) if isinstance(game_id, int) else game_id
    fname = get_fname(game_id)
    if not os.path.isfile(fname):
        return
    with open(fname, "r") as myfile:
        html = myfile.read().replace('\n', '')
    return html


def load_samples(num=None):

    parse_errs = []

    # Get the ids out of space-delimmed jeap_src_ids.txt file.
    src_game_ids = []
    with open(settings.JEAP_ID_FILE) as myfile:
        src_game_ids = myfile.read().split()

    created = 0

    for i, game_id in enumerate(src_game_ids):
        if num and i > num:
            break
        html = read_local_html(game_id)
        if not html:
            continue

        game, errors = parse_game_html(html, game_id)
        created += 1
        if errors:
            parse_errs.append(errors)

        err_count = 0 if not errors else len(errors)
        # print "{}, game:{},  errors:{}".format(i, game, err_count)
        log.debug("%s: %s" % (i, game))

    log.info("Loaded %s J Games, %s parse_errs." % (created, len(parse_errs)))
    return created


def parse_seasons(count=1):
    """Get game_ids from given number of seasons.
    """
    ids = range(count)
    for seas_id in ids:
        url = 'http://www.j-archive.com/showseason.php?season=' + str(seas_id + 1)
        print 'Getting', url
        soup = BeautifulSoup(requests.get(url).text)
        for tag in soup.find_all('a'):
            if 'game_id' in tag['href']:
                match = re.search('\d+', tag['href'])
                if match:
                    # game_ids.append(match.group(0))
                    yield match.group(0)


