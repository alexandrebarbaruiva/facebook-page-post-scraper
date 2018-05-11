import csv
import sys
from page_scraper import Scraper
from token_manager import retrieve_token_file
from get_fb_posts_fb_page import \
    request_until_succeed, getFacebookPageFeedUrl, \
    processFacebookPageFeedStatus, scrapeFacebookPageFeedStatus, \
    scrapAll, write_json


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
                collect_token_automatically(
                    *decrypt_user_password(**retrieve_password_file())
                )
            except Exception as inst:
                self.fail('Token has expired, please renew it.')
        else:
            collect_token_automatically(sys.argv[1:][0], sys.argv[1:][1])
    else:
        for page in pages:
            scraper.set_page(page)
            print(scraper.page)
            scraper.get_page_name_and_like()
            scraper.get_reactions()
            scraper.write_file()
            scraper.convert_to_csv()


if __name__ == '__main__':
    collect_all_pages()
