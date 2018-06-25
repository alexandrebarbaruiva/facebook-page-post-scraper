"""Todas as funções referentes a coleta de dados de várias páginas."""
import os
import csv
from time import strftime
from .page_scraper import Scraper
from .token_manager import retrieve_token_file, get_user_password_decrypted, \
    retrieve_password_file, collect_token_automatically, collect_token
from .get_posts import write_posts_to_csv, write_comments_to_csv


def read_entidades(pages, entidades='entidades'):
    """
    Leitura de todas as entidades desejadas.

    Responsável por coletas todas a entidades em que será feita a
    raspagem de dados.
    """
    with open(entidades + '.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    return pages


def checkin_updating_token():
    """Verifica se o token é válido e atualiza o mesmo caso necessário."""
    scraper = Scraper(retrieve_token_file())

    # Verifica se o token ainda é válido
    if not scraper.check_valid_token():
        # Caso não seja, verifica se existe um config.ini
        if retrieve_password_file():
            collect_token_automatically(*get_user_password_decrypted())
        # Caso não exista o arquivo, dispara a função para gerar o arquivo
        else:
            collect_token()


def collect_all_pages():
    """Raspa informações de todas as páginas."""
    pages = []
    pages = read_entidades(pages)
    checkin_updating_token()
    scraper = Scraper(retrieve_token_file())

    os.chdir("json")
    print(strftime("%Y-%m-%d"))
    if not os.path.exists(strftime("%Y-%m-%d")):
        os.mkdir(strftime("%Y-%m-%d"))
    os.chdir("..")
    if not os.path.exists('csv/' + strftime("%Y-%m-%d")):
        os.mkdir('csv/' + strftime("%Y-%m-%d"))
    for page in pages:
        scraper.set_page(page)
        print(scraper.page)
        scraper.get_page_name_and_like()
        scraper.get_reactions()
        scraper.write_to_json(actor_name=scraper.page)
        scraper.write_to_csv()
        scraper.calldb(actor_name=scraper.page)
    write_posts_to_csv()
    write_comments_to_csv()
    scraper.write_actors_and_date_file()


def collect_new_data():
    """Função usada para checar o formato dos novos dados."""
    new_info = []
    pages = []
    pages = read_entidades(pages)
    new_info = read_entidades(new_info, 'novos_dados')
    checkin_updating_token()
    scraper = Scraper(retrieve_token_file())
    for info in new_info:
        for page in pages:
            scraper.set_page(page)
            print(scraper.page)
            scraper.scrape_current_page(query=info)
            scraper.write_to_csv(info)


if __name__ == '__main__':
    collect_all_pages()
