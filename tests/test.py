import unittest
import os
import sys
import csv
from time import strftime
from scraper.post_scraper import Scraper
from scraper.token_manager import \
    retrieve_token_file, update_token_file, generate_token_file


class TestTokenFunctions(unittest.TestCase):

    def test_if_token_file_exists(self):
        """
        Check if token file exists, if it doesn't, returns warning message
        """
        self.assertFalse(retrieve_token_file('test.txt'))
        if not retrieve_token_file():
            self.fail('Token file missing, please provide a token file.')

    def test_if_token_is_well_formatted(self):
        """
        Check if token file is well formatted
        """
        self.assertEqual(
            retrieve_token_file('badtoken.ini'),
            'Token with bad structure'
        )

    def test_if_token_can_be_updated(self):
        """
        Check if token file can be updated with new token
        """
        generate_token_file(file='default.ini')
        self.assertEqual(
            update_token_file(file='default.ini'),
            'Token not updated.'
        )
        self.assertEqual(
            update_token_file('TestTokenNotValid', file='default.ini'),
            'New token written successfuly.'
        )
        os.remove(str(os.getcwd())+'/scraper/default.ini')

    def test_if_empty_token_file_can_be_generated(self):
        """
        Check if token file generation is generating a correct file
        """
        self.assertEqual(generate_token_file(file='empty.ini')[0], True)
        self.assertEqual(
            generate_token_file(file='empty.ini'),
            [False, 'File already exists']
        )
        os.remove(str(os.getcwd())+'/scraper/empty.ini')

    def test_if_token_file_can_be_generated(self):
        """
        Check if token file can be generated
        """
        new_token = "THISISAGOODTEST"
        self.assertEqual(
            generate_token_file(new_token, file='empty.ini'),
            [True, new_token]
        )
        os.remove(str(os.getcwd())+'/scraper/empty.ini')


class TestPostScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token_file())
        self.github = '262588213843476'

    def tearDown(self):
        self.scraper = None

    def test_if_token_provided_is_valid(self):
        """
        Check if token provided by user hasn't expired
        """
        self.assertTrue(self.scraper.check_valid_token())

    def test_if_status_is_400(self):
        """
        Check if when no page is provided, status is 400
        """
        self.assertTrue(self.scraper.check_status_code(), 400)

    def test_if_page_is_as_provided_by_user(self):
        """
        Check if page provided by user is correctly stored. Example used
        is Github's page
        """
        self.scraper.set_page(self.github)
        self.assertEqual(self.scraper.get_current_page(), '262588213843476')

    def test_if_scraping_page(self):
        """
        Check if scraping is correct and working
        """
        self.scraper.set_page(self.github)
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
        self.assertEqual(
            self.scraper.scrape_current_page(page=self.github, feed=True),
            True
        )
        test_query = 'message,comments.summary(true){likes}'
        self.assertEqual(
            self.scraper.scrape_current_page
            (feed=True, query=test_query), True
        )

    def test_if_scraping_outputs_file(self):
        """
        Check if scraping generates a JSON file in correct output file
        """
        test_query = 'message,comments.summary(true){likes}'
        self.scraper.scrape_current_page(
            page=self.github, feed=True, query=test_query
        )
        self.assertTrue(self.scraper.write_file())
        self.assertTrue(os.path.exists('json/262588213843476.json'))
        os.remove(str(os.getcwd())+'/json/262588213843476.json')

    def test_scraping_name_and_likes(self):
        """
        Check if it's possible to collect name and like from
        facebook page with date of collection
        """
        self.assertEqual(
            self.scraper.get_page_name_and_like('262588213843476'),
            ['GitHub', strftime("%d/%m/%Y")]
        )

    def test_if_csv_without_content_returns_nothing(self):
        """
        Chech if when presented with no content, csv converter returns a
        'No content found' instead of an empty csv
        """
        self.assertEqual(self.scraper.convert_to_csv(), 'No content found.')

    def test_if_conversion_to_csv_happens(self):
        """
        Check if when presented with a page content, csv converter generates
        a csv file with the proper content
        """
        self.scraper.get_page_name_and_like(self.github)
        day_scraped = strftime("%Y%m%d")
        self.assertTrue(self.scraper.convert_to_csv())
        self.assertTrue(
            os.path.exists('csv/scraped_' + day_scraped + '.csv')
        )
        # Check if csv header is as expected
        with open('csv/scraped_' + day_scraped + '.csv') as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                ['name', 'fan_count', 'id', 'date']
            )
            # Check for amount of pages scraped is correct
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 1)
        os.remove(str(os.getcwd())+'/csv/scraped_' + day_scraped + '.csv')

    def test_if_multiple_conversions_generate_one_file(self):
        """
        Check if when presented with multiple page contents, csv converter
        generates only one csv file with the proper content of all pages
        """
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.convert_to_csv()
        self.scraper.get_page_name_and_like('20531316728')
        self.scraper.convert_to_csv()
        self.assertTrue(self.scraper.convert_to_csv())
        day_scraped = strftime("%Y%m%d")
        self.assertTrue(
            os.path.exists('csv/scraped_' + day_scraped + '.csv')
        )
        # Check if csv header is as expected
        with open('csv/scraped_' + day_scraped + '.csv') as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                ['name', 'fan_count', 'id', 'date']
            )
            # Check for amount of pages scraped is correct
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 2)
        os.remove(str(os.getcwd())+'/csv/scraped_' + day_scraped + '.csv')


if __name__ == '__main__':
    unittest.main()
