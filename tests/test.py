import unittest
import os
from scraper.post_scraper import Scraper

class TestPostScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper()

    def test_nothing(self):
        """
        Check if testing is really ocurring
        """
        pass

    def test_if_link_is_online(self):
        self.assertEqual(self.scraper.status_code, 200)

if __name__ == '__main__':
    unittest.main()
