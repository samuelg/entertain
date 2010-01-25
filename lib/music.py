import datetime
import feedparser

MUSIC_URL = 'http://feeds2.feedburner.com/PitchforkAlbumReviews'

def parse_music(json=False):
    """ Parses the lastest 10 albums reviews from pitchfork and returns a dictionary
        in the form {title, link, date}.

        Pass json=True to get albums in JSON format.
    """
    content = feedparser.parse(MUSIC_URL).entries

    return [__cleaned(album, json) for album in content[:10]]

def __cleaned(album, json):
    """
        Cleans the albums data and returns a dictionary in the form {title, link, date}
    """
    link =  album.link
    title = " - ".join(map(lambda x: x.strip(), album.title.split('-')))
    date = datetime.datetime(*album.updated_parsed[:6])

    # convert date to timestamp
    if json:
        date = date.strftime('%a, %d %b %Y')

    return {'title': title, 'link': link, 'date': date}

if __name__ == '__main__':
    """
        command line
    """
    albums = parse_music()
    print albums
