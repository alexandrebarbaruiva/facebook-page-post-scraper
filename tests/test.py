import unittest
import os
from scraper.post_scraper import Scraper, retrieve_token

class TestPostScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token)

    def test_nothing(self):
        """
        Check if testing is really ocurring
        """
        pass

    def test_if_link_is_online(self):
        self.assertEqual(self.scraper.check_status_code(), 404)

if __name__ == '__main__':
    unittest.main()
