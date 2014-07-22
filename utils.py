import requests

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='


def get_page(game_id):
    url = URL_BASE + game_id
    return requests.get(url).text



    # outfile = open('season_ids.txt', 'w')
    # for sid in sids:
    #     outfile.write(sid + '\n')
    # outfile.close()


