import os
import requests
from parser import parse_game
# from models import Clue

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='
SAMPLE_DIR = 'samples'


def parse_game_ids(*game_ids):
    """
    Parse clues from given sample game ids.
    """
    clues = []
    for game_id in game_ids:
        html = get_local_html(game_id)
        if not html:
            continue
        game_clues = list(parse_game(html))
        clues.extend(game_clues)
    return clues


def get_fname(game_id):
    """
    Returns valid sampledir filename for given_id.
    """
    if isinstance(game_id, int):
        game_id = str(game_id)
    return os.path.join(SAMPLE_DIR, "game_{}.html".format(game_id))


def write_game(game_id, html):
    """
    Save html as a file in the SAMPLE_DIR, named by game_id.
    """
    fname = get_fname(game_id)
    if len(html) < 3000:
        print game_id, 'skipped, too short', len(html)
        return

    try:
        with open(get_fname(game_id), "w") as outfile:
            outfile.write(html)
        print "Wrote", fname
    except UnicodeEncodeError as uni_err:
        print uni_err


def get_remote_html(game_id):
    game_id = str(game_id) if isinstance(game_id, int) else game_id
    url = URL_BASE + game_id
    return requests.get(url).text


def save_remote_games(self, *game_ids):
    for game_id in game_ids:
        html = self.get_html(game_id)
        print "L of {} is {}".format(game_id, len(html))
        self.write_game(game_id, html)


def get_local_html(game_id):
    game_id = str(game_id) if isinstance(game_id, int) else game_id
    fname = get_fname(game_id)
    if not os.path.isfile(fname):
        return
    with open(fname, "r") as myfile:
        html = myfile.read().replace('\n', '')
    return html


GAME_IDS = [4529, 368, 4249, 363, 362, 361, 360, 359, 356, 355, 354, 353, 352, 348, 347, 345,
            344, 341, 340, 339, 338, 180, 179, 177, 174, 173, 3377, 4277, 1992, 1991, 4230,
            4281, 4279, 2265, 2264, 2263, 2262, 2205, 4284, 4269, 116, 4271, 4260, 4258, 4254,
            3952, 4267, 4273, 4256, 4261, 902, 900, 3069, 3067, 3065, 3062, 3061, 3060, 3053,
            3051, 4251, 297, 294, 251, 295, 246, 4233, 3455, 3055, 4407, 4236, 4282, 4099, 4275,
            1339, 1338, 1337, 1336, 1335, 3118, 3117, 4083, 4220, 4219, 4217, 4214, 4213, 4085,
            1756, 3943, 4395, 3970, 4244, 4097, 4246, 4247, 4240, 3436, 3568, 4265, 4307, 4533,
            4264, 629, 626, 2555, 3676, 3674, 3671, 3670, 3666, 2482, 3665, 4158, 4157, 3454,
            3501, 3934, 3940, 2813, 4094, 4490, 4091, 2933, 4089, 4080, 4460, 3451, 3450, 4530,
            4412, 3409, 3047, 4564, 4189, 4188, 4525, 4524, 4522, 4515, 4518, 4520, 4513, 4512,
            2867, 1132, 1346, 1345, 1344, 1343, 1342, 4554, 2584, 2583, 4559, 115, 112, 105, 101,
            93, 92, 84, 85, 83, 81, 4286, 4560, 4283, 1135, 4288, 1674, 1673, 1672, 1671, 1670,
            4410, 4296, 4295, 4292, 4291, 4290, 4302, 3573, 4297, 4298, 3711, 182, 181, 178, 170,
            171, 169, 167, 164, 160, 159, 3585, 4475, 4473, 4289, 4491]
