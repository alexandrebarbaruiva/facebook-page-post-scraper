"""All functions related to collecting multiple pages automatically."""
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
    pages = []
    pages = read_entidades(pages)
    checkin_updating_token()
    scraper = Scraper(retrieve_token_file())

    os.chdir("json")
    print(strftime("%Y-%m-%d"))
    if not os.path.exists(strftime("%Y-%m-%d")):
        os.mkdir(strftime("%Y-%m-%d"))
    os.chdir("..")

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


def collect_2018():
    """
    Collects all data from 2018.

    Retrieves all data from 2018 day by day, generates lots of files.
    """
    pages = []
    pages = read_entidades(pages)
    checkin_updating_token()
    scraper = Scraper(retrieve_token_file())

    for page in pages:
        try:
            scraper.set_page(page)
            print(scraper.page)
            for month in range(1, 6):
                for day in range(1, 31):
                    if not scraper.check_valid_token():
                        collect_token_automatically(
                            *get_user_password_decrypted()
                        )
                        scraper = Scraper(retrieve_token_file())
                    if (not scraper.valid_page()):
                        print("Page doesn't exist")
                        break
                    if (month == int(strftime("%m"))) \
                            and (day == (int(strftime("%d")) + 1)):
                        print("end of collection")
                        break
                    try:
                        scraper.get_page_name_and_like()
                        since_date = \
                            strftime("%Y-") + \
                            "{0:02d}".format(month) + "-" + \
                            "{0:02d}".format(day)
                        until_date = \
                            strftime("%Y-") + \
                            "{0:02d}".format(month) + "-" + \
                            "{0:02d}".format(day + 1)
                        print(since_date, until_date)
                        filename = \
                            str(page) + "_" + \
                            strftime("%Y-%m-%d") + "_" + \
                            since_date + "_" + \
                            until_date + ".json"
                        scraper.get_reactions(
                            since_date=since_date, until_date=until_date
                        )
                        scraper.write_to_json(file=filename)
                    except Exception as inst:
                        print("Day {0} not found.".format(day + 1))
                        print(inst)
                        pass
        except Exception as inst:
            print("Page not found.", inst)


def collect_new_data():
    """
    Fuction used to check what sort of output the Graph API generates
    """
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
