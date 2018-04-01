import facebook
import requests
import os
import sys
from configparser import ConfigParser
import logging
import json


def retrieve_token(file='config.ini'):
    """
    Retrives token from config.ini file on scraper folder
    """
    try:
        config = ConfigParser()
        config.read_file(open(str(os.getcwd())+'/scraper/'+file))
        return(config['DEFAULT']['token'])
    except:
        return False


def update_token(new_token=None, file='config.ini'):
    """
    Update token from config.ini file on scraper folder
    """
    if new_token is not None:
        config = ConfigParser()
        config['DEFAULT'] = {'token': new_token}
        with open(str(os.getcwd())+'/scraper/'+file, 'w') as configfile:
            config.write(configfile)
        return 'New token written successfuly.'
    else:
        return 'Token not updated.'


class Scraper:
    """
    Scraper responsible for collecting posts from Facebook
    """
    def __init__(self, token):
        self.token = token
        self.status_code = 400

    def check_valid_token(self):
        """
        Checks if token provided is valid
        """
        url = 'https://graph.facebook.com/v2.12/me?access_token=' \
            + str(self.token)
        r = requests.get(url)
        return(r.status_code == 200)

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

    def get_current_page(self):
        return self.page

    def scrape_current_page(self, feed=False, query=''):
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        feed_statement = '/feed' if feed else ''
        post = graph.get_object(id=self.page+feed_statement, fields=query)
        # print(json.dumps(post, indent=4))
        if 'name' in post.keys():
            return post['name']
        elif 'data' in post.keys():
            return True

    def get_new_token(self):
        pass
