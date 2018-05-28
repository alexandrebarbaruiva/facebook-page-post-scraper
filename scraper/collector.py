import csv
import sys
from time import strftime
from .page_scraper import Scraper
from .token_manager import retrieve_token_file, get_user_password_decrypted, \
    retrieve_password_file, collect_token_automatically, collect_token


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
                collect_token_automatically(*get_user_password_decrypted())
                scraper = Scraper(retrieve_token_file())
            except Exception as inst:
                print(inst)
                return -1
        else:
            try:
                collect_token()
                scraper = Scraper(retrieve_token_file())
            except Exception as inst:
                print(inst)
                return -1

    for page in pages:
        scraper.set_page(page)
        print(scraper.page)
        scraper.get_page_name_and_like()
        scraper.get_reactions()
        scraper.write_to_json()
        scraper.write_to_csv()


def collect_2018():
    pages = []
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    scraper = Scraper(retrieve_token_file())

    for page in pages:
        try:
            scraper.set_page(page)
            print(scraper.page)
            for month in range(1, 6):
                # print("Month {}".format(month))
                for day in range(1, 31):
                    # print("Day {}".format(day))
                    if not scraper.check_valid_token():
                        collect_token_automatically(
                            *get_user_password_decrypted()
                        )
                        scraper = Scraper(retrieve_token_file())
                    if (not scraper.valid_page()):
                        print("Page doesn't exist")
                        break
                    if (month == int(strftime("%m"))) \
                            and (day == (int(strftime("%d"))+1)):
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
                            "{0:02d}".format(day+1)
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
                        print("Day {0} not found.".format(day+1))
                        print(inst)
                        pass
        except Exception as inst:
            print("Page not found.", inst)


def collect_2018():
    pages = []
    with open('entidades.csv', 'r') as entidades:
        reader = csv.reader(entidades)
        for row in reader:
            pages.append(row[0])
    scraper = Scraper(retrieve_token_file())

    for page in pages:
        try:
            scraper.set_page(page)
            print(scraper.page)
            for month in range(1, 6):
                # print("Month {}".format(month))
                for day in range(1, 31):
                    # print("Day {}".format(day))
                    if not scraper.check_valid_token():
                        collect_token_automatically(
                            *get_user_password_decrypted()
                        )
                        scraper = Scraper(retrieve_token_file())
                    if (not scraper.valid_page()):
                        print("Page doesn't exist")
                        break
                    if (month == int(strftime("%m"))) \
                            and (day == (int(strftime("%d"))+1)):
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
                            "{0:02d}".format(day+1)
                        print(since_date, until_date)
                        filename = \
                            str(page) + "_" + \
                            strftime("%Y-%m-%d") + "_" + \
                            since_date + "_" + \
                            until_date + ".json"
                        scraper.get_reactions(
                            since_date=since_date, until_date=until_date
                        )
                        scraper.write_file(file=filename)
                    except Exception as inst:
                        print("Day {0} not found.".format(day+1))
                        print(inst)
                        pass
        except Exception as inst:
            print("Page not found.", inst)


if __name__ == '__main__':
    collect_all_pages()
