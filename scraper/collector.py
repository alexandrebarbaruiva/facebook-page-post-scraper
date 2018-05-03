import csv
from page_scraper import Scraper
from token_manager import retrieve_token_file
from get_fb_posts_fb_page import \
    request_until_succeed, getFacebookPageFeedUrl, processFacebookPageFeedStatus,\
    scrapeFacebookPageFeedStatus, scrapAll, write_json


def collect_all_pages():
    pages = []
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    scraper = Scraper(retrieve_token_file())
    if scraper.check_valid_token():
        for page in pages:
            scraper.set_page(page)
            print(scraper.page)
            scraper.get_page_name_and_like()
            scraper.get_reactions()
            scraper.write_file()
            scraper.convert_to_csv()
    else:
        print('Please renew token')

def collect():
    pages = []
    access_token = str(retrieve_token_file())
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    scraper = Scraper(retrieve_token_file())
    if scraper.check_valid_token():
        for page in pages:
            scrapAll(access_token,page)
    else:
        print('Please renew token')


if __name__ == '__main__':
    collect_all_pages()
    # collect()
    # access_token = str(retrieve_token_file())
    # scrapAll(access_token)

