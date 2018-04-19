import unittest
import os
import sys
from time import strftime
from scraper.post_scraper import Scraper
from scraper.token_manager import \
    retrieve_token, update_token, generate_token_file


class TestTokenFunctions(unittest.TestCase):

    def test_if_token_file_exists(self):
        """
        Check if token file exists, if it doesn't
        """
        self.assertFalse(retrieve_token('test.txt'))
        if not retrieve_token():
            self.fail('Token file missing, please provide a token file.')

    def test_if_token_is_well_formatted(self):
        self.assertEqual(
            retrieve_token('badtoken.ini'),
            'Token with bad structure'
        )

    def test_if_token_can_be_updated(self):
        self.assertEqual(
            update_token(file='default.ini'),
            'Token not updated.'
        )
        self.assertEqual(
            update_token('TestTokenNotValid', file='default.ini'),
            'New token written successfuly.'
        )

    def test_if_empty_token_file_can_be_generated(self):
        self.assertEqual(generate_token_file(file='empty.ini')[0], True)
        self.assertEqual(
            generate_token_file(file='empty.ini'),
            [False, 'File already exists']
        )
        os.remove(str(os.getcwd())+'/scraper/empty.ini')

    def test_if_token_file_can_be_generated(self):
        new_token = "THISISAGOODTEST"
        self.assertEqual(
            generate_token_file(new_token, file='empty.ini'),
            [True, new_token]
        )
        os.remove(str(os.getcwd())+'/scraper/empty.ini')


class TestPostScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token())

    def tearDown(self):
        self.scraper = None

    def test_nothing(self):
        """
        Check if testing is really ocurring
        """
        pass

    def test_if_token_provided_is_valid(self):
        """
        Check if token provided by user hasn't expired
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
        Check if scraping is correct and working
        """
        self.scraper.set_page('262588213843476')
        self.assertEqual(self.scraper.scrape_current_page(), 'GitHub')

    def test_scraping_without_page(self):
        """
        Check if when user doesn't define page, program returns warning
        """
        self.assertEqual(self.scraper.get_current_page(), 'Page not set')
        self.assertEqual(
            self.scraper.scrape_current_page(),
            'Page not defined or bad query structure'
        )

    def test_if_scraping_page_with_queries(self):
        """
        Check if scraping with queries is correct and working correctly
        """
        self.scraper.set_page('262588213843476')
        self.assertEqual(self.scraper.scrape_current_page(feed=True), True)
        test_query = 'message,comments.summary(true){likes}'
        self.assertEqual(
            self.scraper.scrape_current_page
            (feed=True, query=test_query), True
        )

    def test_if_scraping_outputs_file(self):
        self.scraper.set_page('262588213843476')
        test_query = 'message,comments.summary(true){likes}'
        self.scraper.scrape_current_page(feed=True, query=test_query)
        self.assertTrue(self.scraper.write_file(), True)

    def test_scraping_name_and_likes(self):
        """
        Check if it's possible to collect name and like from
        facebook page with date of collection
        """
        self.scraper.set_page('262588213843476')
        self.assertEqual(
            self.scraper.get_page_name_and_like(),
            ['GitHub', strftime("%d/%m/%Y")]
        )


if __name__ == '__main__':
    unittest.main()
