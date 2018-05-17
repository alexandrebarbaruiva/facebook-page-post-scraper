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

from pathlib import Path
home = Path.home()

class TestPageScraperBasics(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token_file())
        self.github = '262588213843476'
        self.day_scraped = strftime("%Y-%m-%d_%Hh")
        if not self.scraper.check_valid_token():
            if retrieve_password_file():
                try:
                    get_user_password_decrypted()
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
        self.csv_dir = home.joinpath('csv')
        self.json_dir = home.joinpath('json')
        self.nome = 'nome'
        self.test = 'test'
        self.react = 'react'
        self.csv_dir_file_nome = self.csv_dir.joinpath('{}_{}.csv'.format(self.nome, self.day_scraped))
        self.csv_dir_file_test = self.csv_dir.joinpath('{}_{}.csv'.format(self.test, self.day_scraped))
        self.csv_dir_file_react = self.csv_dir.joinpath('{}_{}.csv'.format(self.react, self.day_scraped))
        self.json_dir_file_nome_json = self.json_dir.joinpath('{}.json'.format(self.github))
        if not self.scraper.check_valid_token():
            if retrieve_password_file():
                try:
                    collect_token_automatically(
                        *decrypt_user_password(**retrieve_password_file())
                    )
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

    def test_if_scraping_outputs_file(self):
        """
        Check if scraping generates a JSON file in correct output file
        """
        test_query = 'message,comments.summary(true){likes}'
        self.scraper.scrape_current_page(
            page=self.github, feed=True, query=test_query
        )
        self.assertTrue(self.scraper.write_file())
        self.assertTrue(self.json_dir_file_nome_json.is_file(), msg='File not found')
        # Deletar arqquivo na pasta
        if self.json_dir_file_nome_json.is_file():
            self.json_dir_file_nome_json.unlink()
        else:
            print("Arquivo não existe: " + str(self.json_dir_file_nome_json))

    def test_scraping_name_and_likes(self):
        """
        Check if it's possible to collect name and like from
        LearnPython page with date of collection
        """
        self.assertEqual(
            self.scraper.get_page_name_and_like('262588213843476'),
            ['GitHub', strftime("%d/%m/%Y")]
        )

    def test_if_csv_without_content_returns_nothing(self):
        """
        Check if when presented with no content, csv converter returns a
        'No content found' instead of an empty csv
        """
        self.assertEqual(self.scraper.convert_to_csv(), 'No content found.')

    def test_if_conversion_to_csv_happens(self):
        """
        Check if when presented with a page content, csv converter generates
        a csv file with the proper content
        """
        self.scraper.get_page_name_and_like(self.github)
        self.assertTrue(self.scraper.convert_to_csv(self.nome))
        self.assertTrue(self.csv_dir_file_nome.is_file(), msg='File not found')
        # Check if csv header is as expected
        with open(str(self.csv_dir_file_nome)) as file:
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
        if self.csv_dir_file_nome.is_file():
            self.csv_dir_file_nome.unlink()
        else:
            print("Arquivo não existe: " + str(self.csv_dir_file_nome))

    def test_if_multiple_conversions_generate_one_file(self):
        """
        Check if when presented with multiple page contents, csv converter
        generates only one csv file with the proper content of all pages and
        without duplicated pages
        """
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.convert_to_csv('test')
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.convert_to_csv('test')
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.convert_to_csv('test')
        self.assertTrue(self.scraper.convert_to_csv(self.test))
        self.assertTrue(self.csv_dir_file_test.is_file(), msg='File not found')
        # Check if csv header is as expected
        with open(str(self.csv_dir_file_test)) as file:
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
        if self.csv_dir_file_test.is_file():
            self.csv_dir_file_test.unlink()
        else:
            print("Arquivo não existe: " + str(self.csv_dir_file_test))

    def test_if_get_reactions_works(self):
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.get_reactions()
        self.assertTrue(self.scraper.convert_to_csv(self.react))
        with open(str(self.csv_dir_file_react)) as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                [
                    'name', 'id', 'date', 'fan_count', 'total_posts',
                    'total_reactions', 'total_comments', 'total_shares',
                    'average_reactions', 'average_comments'
                ]
            )
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 1)
        # Deletar arqquivo na pasta
        if self.csv_dir_file_react.is_file():
            self.csv_dir_file_react.unlink()
        else:
            print("Arquivo não existe: " + str(self.csv_dir_file_react))

    def test_if_get_reactions_works_with_more_pages(self):
        self.scraper.get_page_name_and_like('262588213843476')
        self.scraper.get_reactions()
        self.scraper.convert_to_csv(self.react)
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.get_reactions()
        self.scraper.convert_to_csv(self.react)
        self.scraper.get_page_name_and_like('135117696663585')
        self.scraper.get_reactions()
        self.scraper.convert_to_csv(self.react)
        self.assertTrue(self.csv_dir_file_react.is_file(), msg='File not found')
        with open(str(self.csv_dir_file_react)) as file:
            reader = csv.reader(file)
            self.assertEqual(
                next(reader),
                [
                    'name', 'id', 'date', 'fan_count', 'total_posts',
                    'total_reactions', 'total_comments', 'total_shares',
                    'average_reactions', 'average_comments'
                ]
            )
            pages = 0
            for row in reader:
                pages += 1
            self.assertEqual(pages, 2)
        # Deletar arqquivo na pasta
        if self.csv_dir_file_react.is_file():
            self.csv_dir_file_react.unlink()
        else:
            print("Arquivo não existe: " + str(self.csv_dir_file_react))

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
