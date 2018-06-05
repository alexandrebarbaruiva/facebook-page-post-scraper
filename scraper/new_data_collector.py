import csv
import sys
from time import strftime
from .page_scraper import Scraper
from .token_manager import retrieve_token_file, get_user_password_decrypted, \
    retrieve_password_file, collect_token_automatically
from .collector import read_entidades, checkin_updating_token
import os


def collect_new_data():
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
    collect_new_data()
