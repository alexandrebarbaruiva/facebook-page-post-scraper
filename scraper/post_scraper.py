import facebook
import requests
import sys
import json


class Scraper:
    """
    Scraper responsible for collecting posts from Facebook
    """
    def __init__(self, token):
        self.token = token
        self.status_code = 400
        # self.current_data = 'NO DATA'

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
        self.file_name = (str(self.page)+'.json')

    def get_current_page(self):
        try:
            return self.page
        except:
            return 'Page not defined'

    def scrape_current_page(self, feed=False, query=''):
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        feed_statement = '/feed' if feed else ''
        try:
            post = graph.get_object(id=self.page+feed_statement, fields=query)
            self.current_data = post
            if 'name' in post.keys():
                return post['name']
            elif 'data' in post.keys():
                return True
        except:
            return 'Page not defined'

    def write_file(self, file=None):
        if file is None:
            file = self.file_name
        with open(file, 'w') as data_file:
            data_file.write(
                json.dumps(self.current_data, indent=2)
            )  # pretty json
            return True

    def get_new_token(self):
        pass
