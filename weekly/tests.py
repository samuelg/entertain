from django.test import TestCase
from django.core.urlresolvers import reverse
from lib import music

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
        self.assertTrue(response.context[-1]['albums'])

    def test_music(self):
        """
            Tests the music library.
        """
        albums = music.parse_music()
        self.assertTrue(albums)
        self.assertEquals(10, len(albums))

