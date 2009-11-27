import urllib2
import datetime
from beautifulsoup import BeautifulSoup

MUSIC_URL = 'http://feeds2.feedburner.com/PitchforkAlbumReviews'

def parse_music():
    """ Parses the lastest 10 albums reviews from pitchfork and returns a dictionary
        in the form {title, link, date}
    """
    music = urllib2.urlopen(MUSIC_URL)
    html = BeautifulSoup(music)
    content = html.findAll('item')

    return [__cleaned(album) for album in content[:10]]

def __cleaned(album):
    """
        Cleans the albums data and returns a dictionary in the form {title, link, date}
    """
    link =  album.find('feedburner:origlink').string
    title = " - ".join(map(lambda x: x.strip(), album.title.string.split('-')))
    date = datetime.datetime.strptime(album.pubdate.string[5:16], '%d %b %Y')
    
    return {'title': title, 'link': link, 'date': date}

if __name__ == '__main__':
    """
        command line
    """
    albums = parse_music()
    print albums
