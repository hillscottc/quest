import requests

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='


def trim(txt):
    if txt and len(txt) > 10:
        return txt[:9] + '...'


def save_game(game_id):
    url = URL_BASE + game_id
    html = requests.get(url).text
    outfile = open('samples/game_{}.html'.format(game_id), 'w')
    outfile.write(html)
    outfile.close()

# def get_page(game_id):
#     url = URL_BASE + game_id
#     return requests.get(url).text



    # outfile = open('season_ids.txt', 'w')
    # for sid in sids:
    #     outfile.write(sid + '\n')
    # outfile.close()


