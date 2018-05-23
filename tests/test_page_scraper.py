import unittest
import os
import sys
import csv
from time import strftime
from scraper.page_scraper import Scraper
from scraper.token_manager import \
    retrieve_token_file, update_token_file, generate_token_file,\
    retrieve_password_file, encrypt_user_password, \
    collect_token_automatically, decrypt_user_password, \
    get_user_password_decrypted


class TestPageScraperBasics(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token_file())
        self.github = '262588213843476'
        self.day_scraped = strftime("%Y-%m-%d_%Hh")
        if not self.scraper.check_valid_token():
            if retrieve_password_file():
                try:
                    collect_token_automatically(*get_user_password_decrypted())
                except Exception as inst:
                    print(inst)
                    self.fail('Token has expired, please renew it.')
            else:
                self.fail('There is no token.')

    def tearDown(self):
        self.scraper = None

    def test_if_token_provided_is_valid(self):
        """
        Check if token provided by user hasn't expired
        """
        self.assertTrue(self.scraper.check_valid_token())

    def test_if_page_is_as_provided_by_user(self):
        """
        Check if page provided by user is correctly stored. Example used
        is Github's page
        """
        self.scraper.set_page(self.github)
        self.assertEqual(self.scraper.get_current_page(), '262588213843476')


class TestPageScraping(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token_file())
        self.github = '262588213843476'
        self.day_scraped = strftime("%Y-%m-%d_%Hh")
        if not self.scraper.check_valid_token():
            if retrieve_password_file():
                try:
                    collect_token_automatically(*get_user_password_decrypted())
                except Exception as inst:
                    print(inst)
                    self.fail('Token has expired, please renew it.')
            else:
                self.fail('There is no token.')

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

    def test_scraping_name_and_likes(self):
        """
        Check if it's possible to collect name and like from
        LearnPython page with date of collection
        """
        self.assertEqual(
            self.scraper.get_page_name_and_like('262588213843476'),
            ['GitHub', strftime("%Y-%m-%d")]
        )

    def test_if_scraping_outputs_file(self):
        """
        Check if scraping generates a JSON file in correct output file
        """
        test_query = 'message,comments.summary(true){likes}'
        print('json/'+strftime("%Y-%m-%d")+'/262588213843476.json')
        self.scraper.scrape_current_page(
            page=self.github, feed=True, query=test_query
        )
        self.assertTrue(self.scraper.write_to_json())
        self.assertTrue(
            os.path.exists('json/'+strftime("%Y-%m-%d")+'/262588213843476.json'),
            msg='File not found.'
        )
        #Deletar arquivo na pasta
        try:
            os.remove(str(os.getcwd())+'json/' + 
                    strftime("%Y-%m-%d") + '/262588213843476.json')
        except FileNotFoundError:
            pass


    def test_if_csv_without_content_returns_nothing(self):
        """
        Check if when presented with no content, csv converter returns a
        'No content found' instead of an empty csv
        """
        self.assertEqual(self.scraper.write_to_csv(), 'No content found.')

    def test_if_writing_to_csv_happens(self):
        """
        Check if when presented with a page content, csv writer generates
        a csv file with the proper content
        """
        self.scraper.get_page_name_and_like(self.github)
        self.assertTrue(self.scraper.write_to_csv('nome'))
        self.assertTrue(
            os.path.exists('csv/nome_' + self.day_scraped + '.csv'),
            msg='File not found'
        )
        # Check if csv header is as expected
        with open('csv/nome_' + self.day_scraped + '.csv') as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                ['name', 'id', 'date', 'fan_count']
            )
            # Check for amount of pages scraped is correct
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 1)
        # Deletar arqquivo na pasta
        try:
            os.remove(
                str(os.getcwd())+'/csv/nome_' + self.day_scraped + '.csv'
            )
        except FileNotFoundError:
            pass

    def test_if_multiple_writings_generate_one_file(self):
        """
        Check if when presented with multiple page contents, csv writer
        generates only one csv file with the proper content of all pages and
        without duplicated pages
        """
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.write_to_csv('test')
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.write_to_csv('test')
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.write_to_csv('test')
        self.assertTrue(self.scraper.write_to_csv('test'))
        self.assertTrue(
            os.path.exists('csv/test_' + self.day_scraped + '.csv'),
            msg='File not found'
        )
        # Check if csv header is as expected
        with open('csv/test_' + self.day_scraped + '.csv') as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                ['name', 'id', 'date', 'fan_count']
            )
            # Check for amount of pages scraped is correct
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 2)
        # Deletar arqquivo na pasta
        try:
            os.remove(
                str(os.getcwd())+'/csv/test_' + self.day_scraped + '.csv'
            )
        except FileNotFoundError:
            pass

    def test_if_get_reactions_works(self):
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.get_reactions()
        self.assertTrue(self.scraper.write_to_csv('react'))
        with open('csv/react_' + self.day_scraped + '.csv') as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                [
                    'name', 'id', 'date', 'since_date', 'until_date',
                    'fan_count', 'total_posts', 'total_reactions',
                    'total_comments', 'total_shares', 'average_reactions',
                    'average_comments'
                ]
            )
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 1)
        try:
            os.remove(
                str(os.getcwd())+'/csv/react_' + self.day_scraped + '.csv'
            )
        except FileNotFoundError:
            pass

    def test_if_get_reactions_works_with_more_pages(self):
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.get_reactions()
        self.scraper.write_to_csv('react')
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.get_reactions()
        self.scraper.write_to_csv('react')
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.get_reactions()
        self.scraper.write_to_csv('react')
        self.assertTrue(
            os.path.exists('csv/react_' + self.day_scraped + '.csv'),
            msg='File not found'
        )
        with open('csv/react_' + self.day_scraped + '.csv') as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                [
                    'name', 'id', 'date', 'since_date', 'until_date',
                    'fan_count', 'total_posts', 'total_reactions',
                    'total_comments', 'total_shares', 'average_reactions',
                    'average_comments'
                ]
            )
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 2)
        # Deletar arqquivo na pasta
        try:
            os.remove(
                str(os.getcwd())+'/csv/react_' + self.day_scraped + '.csv'
            )
        except FileNotFoundError:
            pass

    def test_if_valid_page_works(self):
        """
        Check if the page validation is working
        """
        self.assertFalse(self.scraper.valid_page("FrenteBrasilPopula"))
        self.assertTrue(self.scraper.valid_page(self.github))
        self.scraper.set_page(self.github)
        self.assertTrue(self.scraper.valid_page())

    def test_get_reactions_with_invalid_page(self):
        """
        Check if when presented with a invalid page get_reactions returns an
        error message
        """
        self.assertEqual(
            self.scraper.get_reactions('FrenteBrasilPopula'),
            "Page is not valid."
        )


if __name__ == '__main__':
    unittest.main()
