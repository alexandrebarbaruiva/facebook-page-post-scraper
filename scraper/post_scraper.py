import facebook
import os
import requests
import sys
import json
import csv
from time import strftime


class Scraper:
    """
    Scraper responsible for collecting posts from Facebook
    """
    def __init__(self, token):
        self.token = token
        self.status_code = 400
        self.current_data = ''
        if not os.path.exists('csv/'):
            os.makedirs('csv/')
        if not os.path.exists('json/'):
            os.makedirs('json/')

    def check_valid_token(self):
        """
        Checks if token provided is valid
        """
        url = 'https://graph.facebook.com/v2.12/me?access_token=' \
            + str(self.token)
        r = requests.get(url)
        return(r.status_code)

    def check_status_code(self):
        """
        Checks for page status code, good for testing if page and query are
        adequate. There's room for improvement here.
        """
        return self.status_code

    def set_page(self, page):
        """
        Set which page to scrape, useful for when having multiple pages
        to scrape.
        """
        self.page = page
        self.file_name = (str(self.page)+'.json')

    def get_current_page(self):
        try:
            return self.page
        except Exception as inst:
            return 'Page not set'

    def scrape_current_page(self, page=None, feed=False, query=''):
        if page is not None:
            self.set_page(page)
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        feed_statement = '/feed' if feed else ''
        try:
            post = graph.get_object(

                    id=str(self.page)+feed_statement,
                    fields=query
            )
            self.current_data = post
            self.current_data['date'] = strftime("%d/%m/%Y")
            # print(self.current_data)
            if 'name' in post.keys():
                return post['name']
            elif 'data' in post.keys():
                return True
        except Exception as inst:
            return 'Page not defined or bad query structure'

    def write_file(self, file=None):
        if file is None:
            file = self.file_name
        with open('json/'+file, 'w', encoding='utf8') as data_file:
            data_file.write(
                json.dumps(self.current_data, indent=2, ensure_ascii=False)
            )  # pretty json
            return True

    def get_page_name_and_like(self, page=None):
        self.scrape_current_page(page, query='name,fan_count')
        return([
            self.current_data['name'],
            # self.current_data['fan_count'],
            # self.current_data['id'],
            strftime("%d/%m/%Y")
        ])

    def convert_to_csv(self, file_name='scraped'):
        def dict_to_list():
            content = []
            for column in column_names:
                content.append(str(self.current_data[column]))
            return content
        try:
            column_names = self.current_data.keys()
        except Exception as inst:
            return ('No content found.')
        today = strftime("%Y%m%d")

        # Check if file already exists to append instead of create
        if os.path.exists('csv/{}_{}.csv'.format(file_name, today)):
            content = dict_to_list()
            # Check if content already exists in csv
            with open(
                    'csv/{}_{}.csv'.format(file_name, today), 'r') as csvfile:
                reader = csv.reader(csvfile)
                reader_list = list(reader)
                for row in reader_list:
                    if row == content:
                        return True
            # Write content on CSV because it's not duplicated
            with open(
                    'csv/{}_{}.csv'.format(file_name, today), 'a') as csvfile:
                info = csv.writer(csvfile)
                info.writerow(content)
            return True

        # Create file because file doesn't exist
        with open('csv/{}_{}.csv'.format(file_name, today), 'w') as csvfile:
            info = csv.writer(csvfile)
            content = dict_to_list()
            info.writerow(column_names)
            info.writerow(content)
        return True
