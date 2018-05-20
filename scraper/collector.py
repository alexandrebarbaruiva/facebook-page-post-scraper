import csv
import sys
from .page_scraper import Scraper
from .token_manager import retrieve_token_file, get_user_password_decrypted, \
    retrieve_password_file


def collect_all_pages():

    pages = []
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    scraper = Scraper(retrieve_token_file())
    if not scraper.check_valid_token():
        if retrieve_password_file():
            try:
                get_user_password_decrypted()
                scraper = Scraper(retrieve_token_file())
            except Exception as inst:
                print(inst)
                raise inst

    for page in pages:
        scraper.set_page(page)
        print(scraper.page)
        scraper.get_page_name_and_like()
        scraper.get_reactions()
        scraper.write_file()
        scraper.convert_to_csv()


if __name__ == '__main__':
    collect_all_pages()
