import unittest
import os
from scraper.post_scraper import Scraper, retrieve_token


class TestPostScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token())

    def test_nothing(self):
        """
        Check if testing is really ocurring
        """
        pass

    def test_if_token_file_exists(self):
        if not retrieve_token():
            self.fail("Token file missing, please provide a token file.")

    def test_if_token_is_valid(self):
        """
        Check if token provided by user is valid
        """
        self.assertTrue(self.scraper.check_valid_token())

    def test_if_status_is_400(self):
        """
        Check if when no page is provided, status is 400
        """
        self.assertEqual(self.scraper.check_status_code(), 400)

    def test_if_page_is_as_provided_by_user(self):
        """
        Check if page provided by user is correctly stored. Example used
        is Github's page
        """
        self.scraper.set_page('262588213843476')
        self.assertEqual(self.scraper.get_current_page(), '262588213843476')

    def test_if_scraping_page(self):
        """
        Check if scraping is correct
        """
        self.scraper.set_page('262588213843476')
        self.assertEqual(self.scraper.scrape_current_page(),'GitHub')


if __name__ == '__main__':
    unittest.main()
