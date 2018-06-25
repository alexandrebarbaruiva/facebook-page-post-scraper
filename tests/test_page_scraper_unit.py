import unittest
import os
import csv
from time import strftime
from scraper.page_scraper import Scraper
from scraper.token_manager import \
    retrieve_token_file, retrieve_password_file, \
    collect_token_automatically, get_user_password_decrypted
from platform import system


class TestPageScraperBasics(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper("token")
        self.github = '262588213843476'
        self.day_scraped = strftime("%Y-%m-%d_%Hh")
        self.scraper.status_code = 200

    def tearDown(self):
        self.scraper = None

    def test_if_page_is_as_provided_by_user(self):
        """
        Checa se a pagina que o usuario escolhe é salva corretamente.
        Exemplo com a pagina do Github
        """
        self.scraper.set_page(self.github)
        self.assertEqual(self.scraper.get_current_page(), '262588213843476')

    def test_check_valid_token(self):
        """
        Checa se a função check valid token funciona
        """
        self.assertTrue(self.scraper.check_valid_token())


class TestWriteFunctions(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper(retrieve_token_file())
        self.github = '262588213843476'
        self.day_scraped = strftime("%Y-%m-%d_%Hh")
        self.scraper.current_data = {
            'name': 'GitHub',
            'fan_count': 163702,
            'id': '262588213843476',
            'date': '2018-06-19'
        }
        self.scraper.file_name = "262588213843476"

    def test_if_scraping_outputs_file(self):
        """
        Checa se a raspagem gera um arquivo JSON com a saida correta.
        """
        test_query = 'message,comments.summary(true){likes}'
        os.chdir("json")
        if not os.path.exists(strftime("%Y-%m-%d")):
            os.mkdir(strftime("%Y-%m-%d"))
        os.chdir("..")
        self.assertTrue(self.scraper.write_to_json())
        self.assertTrue(
            os.path.exists('json/' + strftime("%Y-%m-%d") +
                           '/262588213843476.json'),
            msg='File not found.'
        )
        # Deletar arquivo na pasta
        try:
            os.remove(str(os.getcwd()) + '/json/' +
                      strftime("%Y-%m-%d") + '/262588213843476.json')
        except FileNotFoundError:
            pass
        try:
            os.rmdir(str(os.getcwd()) + '/json/' +
                     strftime("%Y-%m-%d") + '/')
        except OSError:
            pass

    def test_if_csv_without_content_returns_nothing(self):
        """
        Checa se ao não ter nenhum conteudo, csv retorna 'no content found'
        ao inves de criar um csv vazio.
        """
        self.scraper.current_data = ''
        self.assertEqual(self.scraper.write_to_csv(), 'No content found.')

    def test_if_writing_to_csv_happens(self):
        """
        Checa se cria um csv com o conteudo desejado.
        """
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
            if system() == 'Linux' or system() == 'Darwin':
                self.assertEqual(pages, 1)
            elif system() == 'Windows':
                self.assertEqual(pages, 3)
        # Deletar arqquivo na pasta
        try:
            os.remove(
                str(os.getcwd()) + '/csv/nome_' + self.day_scraped + '.csv'
            )
        except FileNotFoundError:
            pass

    def test_if_multiple_writings_generate_one_file(self):
        """
        Checa se quando requisitado por varias paginas,
        se é criado apenas um arquivo ao inves de gerar varios
        arquivos diferentes.
        """
        self.scraper.write_to_csv('test')
        self.scraper.current_data = {
            'name': 'Tchau',
            'fan_count': 163702,
            'id': '135117696663585',
            'date': '2018-06-19'
        }
        self.scraper.write_to_csv('test')
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
            if system() == 'Linux' or system() == 'Darwin':
                self.assertEqual(pages, 2)
            elif system() == 'Windows':
                self.assertEqual(pages, 5)
        # Deletar arqquivo na pasta
        try:
            os.remove(
                str(os.getcwd()) + '/csv/test_' + self.day_scraped + '.csv'
            )
        except FileNotFoundError:
            pass

    def test_get_reactions_with_invalid_page(self):
        """
        Checa se ao informar uma pagina invalida, get_reactions retorna
        mensagem de erro.
        """
        self.assertEqual(
            self.scraper.get_reactions('FrenteBrasilPopula'),
            "Page is not valid."
        )


if __name__ == '__main__':
    unittest.main()
