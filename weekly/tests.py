from django.test import TestCase
from django.core.urlresolvers import reverse
from lib import music
from lib import games

class WeeklyTest(TestCase):
    """
        Tests for weekly app.
    """

    def test_default(self):
        """
        Tests the default view.
        """
        response = self.client.get(reverse('weekly_default'))
        self.assertEquals(response.status_code, 200)
        # self.assertTrue(response.context[-1]['x360_games'])

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

    def test_games(self):
        """
            Tests the games library.
        """
        x360_games = games.parse_games()
        self.assertTrue(x360_games)
        self.assertEquals(10, len(x360_games))
        self.assertTrue(x360_games[0]['title'])
        self.assertTrue(x360_games[0]['link'])
        self.assertTrue(x360_games[0]['date'])

