from django.test import TestCase
from django.core.urlresolvers import reverse
from lib import music
from lib import games
from redis import Redis
import datetime

MUSIC_KEY = 'music:latest'
GAMES_KEY = 'games:latest'

class WeeklyTest(TestCase):
    """
        Tests for weekly app.
    """
    def setUp(self):
        r = Redis(db=9)
        systems = ('xbox', 'wii', 'ds', 'ps3', 'pc')

        r.delete(MUSIC_KEY)
        for system in systems:
            r.delete('%s%s'%(GAMES_KEY, system))
        r.save()

    def test_default(self):
        """
        Tests the default view.
        """
        response = self.client.get(reverse('weekly_default'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['systems'])

    def test_music_notcached(self):
        """
            Tests the music view fetching music that is not cached in Redis.
        """
        r = Redis(db=9)
        response = self.client.get(reverse('weekly_music'))
        results = r.lrange(MUSIC_KEY, 0, -1)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(results)
        self.assertTrue(response.content)
        self.assertEquals(results[0].split('|')[3], datetime.datetime.today().strftime('%a, %d %b %Y'))

    def test_music_cached(self):
        """
            Tests the music view fetching music that is cached in Redis.
        """
        r = Redis(db=9)
        two_days_ago = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime('%a, %d %b %Y')
        r.push(MUSIC_KEY, '%s|%s|%s|%s'%('title','link','date', two_days_ago)) 
        response = self.client.get(reverse('weekly_music'))
        results = r.lrange(MUSIC_KEY, 0, -1)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(results)
        self.assertTrue(response.content)
        self.assertNotEquals(results[0].split('|')[3], two_days_ago)

    def test_games_notcached(self):
        """
            Tests the games view fetching games that are not cached in Redis.
        """
        systems = ('xbox', 'wii', 'ds', 'ps3', 'pc')

        r = Redis(db=9)
        for system in systems:
            key = '%s%s'%(GAMES_KEY, system)
            response = self.client.get(reverse('weekly_games', kwargs={'category': system}))
            results = r.lrange(key, 0, -1)

            self.assertEquals(response.status_code, 200)
            self.assertTrue(results)
            self.assertTrue(response.content)
            self.assertEquals(results[0].split('|')[3], datetime.datetime.today().strftime('%a, %d %b %Y'))

    def test_games_cached(self):
        """
            Tests the games view fetching games that are cached in Redis.
        """
        systems = ('xbox', 'wii', 'ds', 'ps3', 'pc')

        r = Redis(db=9)
        for system in systems:
            key = '%s%s'%(GAMES_KEY, system)
            two_days_ago = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime('%a, %d %b %Y')
            r.push(key, '%s|%s|%s|%s'%('title','link','date', two_days_ago)) 
            response = self.client.get(reverse('weekly_games', kwargs={'category': system}))
            results = r.lrange(key, 0, -1)

            self.assertEquals(response.status_code, 200)
            self.assertTrue(results)
            self.assertTrue(response.content)
            self.assertNotEquals(results[0].split('|')[3], two_days_ago)

    def test_music(self):
        """
            Tests the music library.
        """
        albums = music.parse_music()
        self.assertTrue(albums)
        self.assertEquals(10, len(albums))
        self.assertTrue(albums[0]['title'])
        self.assertTrue(albums[0]['link'])
        self.assertTrue(albums[0]['date'])

    def test_music_json(self):
        """
            Tests the music library returning json format.
        """
        albums = music.parse_music(json=True)
        self.assertTrue(albums)
        albums = list(albums)
        self.assertEquals(10, len(albums))
        self.assertTrue(albums[0]['title'])
        self.assertTrue(albums[0]['link'])
        self.assertTrue(albums[0]['date'])

    def test_games(self):
        """
            Tests the games library.
        """
        systems = ('xbox', 'wii', 'ds', 'ps3', 'pc')

        for system in systems:
            game_results = games.parse_games(system)
            self.assertTrue(game_results)
            self.assertEquals(10, len(game_results))
            self.assertTrue(game_results[0]['title'])
            self.assertTrue(game_results[0]['link'])
            self.assertTrue(game_results[0]['date'])

    def test_games_json(self):
        """
            Tests the games library returning json format.
        """
        systems = ('xbox', 'wii', 'ds', 'ps3', 'pc')

        for system in systems:
            game_results = games.parse_games(system, json=True)
            self.assertTrue(game_results)
            game_results = list(game_results)
            self.assertEquals(10, len(game_results))
            self.assertTrue(game_results[0]['title'])
            self.assertTrue(game_results[0]['link'])
            self.assertTrue(game_results[0]['date'])

