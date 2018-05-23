import csv
import sys
from time import strftime
from page_scraper import Scraper
from token_manager import retrieve_token_file, get_user_password_decrypted, \
    retrieve_password_file, collect_token_automatically


def collect_new_data():
    new_info = []
    pages = []
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    with open('novos_dados.csv', 'r') as to_collect:
        reader = csv.reader(to_collect)
        for row in reader:
            new_info.append(row[0])
    scraper = Scraper(retrieve_token_file())
    if not scraper.check_valid_token():
        if retrieve_password_file():
            try:
                collect_token_automatically(*get_user_password_decrypted())
                scraper = Scraper(retrieve_token_file())
            except Exception as inst:
                print(inst)
                return -1
    for info in new_info:
        for page in pages:
            scraper.set_page(page)
            print(scraper.page)
            scraper.scrape_current_page(query=info)
            scraper.write_csv(info)


if __name__ == '__main__':
    collect_new_data()
