import datetime
import feedparser

BASE_GAMES_URL = 'http://www.metacritic.com/rss/games/'
SYSTEMS = ( 'xbox360.xml',
            'wii.xml',
            'ds.xml'
          )

def parse_games(json=False):
    """ Parses the lastest 10 xbox 360, wii, and DS games from metacritic and returns a dictionary
        in the form {title, link, date}

        Pass json=True to get games in JSON format.
    """

    results = []
    content = map(lambda x: feedparser.parse('%s%s' % (BASE_GAMES_URL, x)).entries[:10], SYSTEMS)
    for game_system in content:
        for game in game_system:
            results.append(__cleaned(game, json))

    return results

def __cleaned(game, json):
    """
        Cleans the games data and returns a dictionary in the form {title, link, date}
    """
    link = game.link
    title = " - ".join(map(lambda x: x.strip(), game.title.split('-')))
    date = datetime.datetime(*game.updated_parsed[:6])

    # convert date to timestamp
    if json:
        date = date.strftime('%a, %d %b %Y')
    
    return {'title': title, 'link': link, 'date': date}

if __name__ == '__main__':
    """
        command line
    """
    games = parse_games()
    print games
