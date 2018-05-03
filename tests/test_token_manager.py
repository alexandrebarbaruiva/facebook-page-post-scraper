import os
import sys
import csv
import requests
import unittest
from time import strftime
from unittest.mock import patch
from scraper.page_scraper import Scraper
from scraper.token_manager import \
    retrieve_token_file, update_token_file, generate_token_file, \
    retrieve_password_file, encrypt_user_password, decrypt_user_password, \
    collect_token_manually, collect_token_automatically, \
    check_automatic_collection


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

    def test_if_token_file_can_be_updated(self):
        """
        Check if token file can be updated with new token
        """
        generate_token_file(file='default.ini')
        self.assertEqual(
            update_token_file(file='default.ini'),
            'File not updated.'
        )
        self.assertEqual(
            update_token_file(
                file='default.ini',
                **{'token': 'TestTokenNotValid'}
            ),
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


class TestTokenSecurity(unittest.TestCase):

    def test_if_token_has_password(self):
        self.assertFalse(retrieve_password_file('test.txt'))
        if not retrieve_password_file():
            self.fail('No user/password informed. Use autotoken.')

    def test_encrypt_user_password(self):
        user = 'teste'
        password = '1234'
        self.assertEqual(type(encrypt_user_password(user, password)), type({}))
        self.assertEqual(len(encrypt_user_password(user, password)), 3)

    def test_decrypt_user_password(self):
        user = 'teste'
        password = '1234'
        encrypted = encrypt_user_password(user, password)
        self.assertEqual(type(decrypt_user_password(**encrypted)), type([]))
        self.assertEqual(len(decrypt_user_password(**encrypted)), 2)

    def test_if_token_can_be_updated_with_password(self):
        user = 'teste'
        password = '1234'
        generate_token_file(file='default.ini')
        self.assertEqual(
            update_token_file(
                file='default.ini',
                **(encrypt_user_password(user, password))
            ),
            'User and password updated.'
        )
        os.remove(str(os.getcwd())+'/scraper/default.ini')


class TestTokenCollection(unittest.TestCase):

    def test_collect_token_manually(self):
        user_input = 'EDA0EdEloEse0cB'
        with patch('builtins.input', return_value=user_input):
            self.assertEqual(
                type(collect_token_manually(file='default.ini')),
                type(Scraper(''))
            )

    def test_collect_token_automatically_with_wrong_id(self):
        self.assertEqual(
            collect_token_automatically(
                'user', 'hugepasswordwithnumbers123', file='default.ini'
            ),
            'Wrong Facebook user or password'
        )

    def test_collect_token_automatically_with_correct_id(self):
        if retrieve_password_file():
            user, password = decrypt_user_password(**retrieve_password_file())
            self.assertEqual(
                type(collect_token_automatically(user, password)),
                type(Scraper(''))
            )
        else:
            self.fail('No user/password informed. Use autotoken.')

    def test_collect_token_automatically_without_internet(self):
        url = 'https://www.google.com/'
        if requests.get(url).status_code != 200:
            user, password = decrypt_user_password(**retrieve_password_file())
            self.assertEqual(
                collect_token_automatically(
                    'user', 'hugepassword', 'default.ini'
                ),
                'Não foi possível abrir o Facebook. Você está online?'
            )
        else:
            pass

    def test_check_function_for_automatic_token(self):
        if retrieve_password_file():
            self.assertEqual(check_automatic_collection('config.ini'), True)
        else:
            self.fail('No user/password informed. Use autotoken.')
