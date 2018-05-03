import facebook
import os
import requests
import sys
import json
import csv
import datetime
import time
from time import strftime
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

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
        if (self.status_code is not 200):
            url = 'https://graph.facebook.com/v2.12/me?access_token=' \
                + str(self.token)
            self.status_code = requests.get(url).status_code
        return(self.status_code == 200)

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
            if set(column_names) == {'name', 'fan_count', 'id', 'date', 'total_reactions',
                 'total_comments', 'total_shares' , 'total_posts' , 'media_reactions' , 'media_comments'}:
                column_names = ['name', 'id', 'fan_count', 'date' , 'total_reactions' , 
                'total_comments' , 'total_shares' , 'total_posts', 'media_reactions' , 'media_comments']
        except Exception as inst:
            return ('No content found.')
        today = strftime("%Y-%m-%d_%Hh")

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
    
    def request_until_succeed(self, url):
        req = Request(url)
        success = False
        while success is False:
            try:
                response = urlopen(req)
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                print(e)
                time.sleep(5)

                print("Error for URL {}: {}".format(url, datetime.datetime.now()))
                print("Retrying.")

        return response.read()

    def processFacebookPageFeedStatus(self, status,t_reaction,t_comments,t_shares):

        # The status is now a Python dictionary, so for top-level items,
        # we can simply call the key.

        # Additionally, some items may not always exist,
        # so must check for existence first

        # Time needs special care since a) it's in UTC and
        # b) it's not easy to use in statistical programs.
        status_id = status['id']

        status_published = datetime.datetime.strptime(
            status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
        status_published = status_published + \
            datetime.timedelta(hours=-3)  # Brasilia time
        status_published = status_published.strftime(
            '%Y-%m-%d %H:%M:%S')  # Converting from the way facebook gives us the created time to a more readable

        # Nested items require chaining dictionary keys.

        num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
        num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status else status['shares']['count']
        t_reaction = t_reaction + num_reactions
        t_comments = t_comments + num_comments
        t_shares = t_shares + num_shares

        return (status_id,status_published, num_reactions, num_comments, num_shares, t_reaction,t_comments,t_shares)
    
    def get_reactions(self, page= None, file=None):
        #if file is None:
         #   file = self.file_name
        #with open('json/'+file, 'w', encoding='utf8') as data_file:
           # data_file.write(
            #    json.dumps(self.current_data, indent=2, ensure_ascii=False)
            #)  # pretty json
            #data_file.write("status_id , status_published , num_reactions ," + \
            #        "num_comments, num_shares , total reaction , total comments , total shares")
            # input date formatted as YYYY-MM-DD
            since_date = "2018-04-20"
            until_date = strftime("%Y-%m-%d")
            t_reaction = 0
            t_comments = 0
            t_shares = 0
            t_posts = 0
            has_next_page = True
            num_processed = 0
            after = ''
            base = "https://graph.facebook.com/v2.12"
            node = "/{}/posts".format(self.page)
            parameters = "/?limit={}&access_token={}".format(100, self.token)
            since = "&since={}".format(since_date) if since_date \
                is not '' else ''
            until = "&until={}".format(until_date) if until_date \
                is not '' else ''
            while has_next_page:
                after = '' if after is '' else "&after={}".format(after)
                base_url = base + node + parameters + after + since + until
                fields = "&fields=message,created_time,type,id," + \
                    "comments.limit(0).summary(true),shares,reactions" + \
                    ".limit(0).summary(true)"
                url1 = base_url + fields
                statuses = json.loads(self.request_until_succeed(url1))

                for status in statuses['data']:
                    # Ensure it is a status with the expected metadata
                    if 'reactions' in status:
                        status_data = self.processFacebookPageFeedStatus(status,t_reaction,t_comments,t_shares)
                        t_reaction = status_data[5]
                        t_comments = status_data[6]
                        t_shares =  status_data[7]
                        t_posts += 1
                    num_processed += 1
                    if num_processed % 100 == 0:
                        print("{} Statuses Processed: {}".format
                            (num_processed, datetime.datetime.now()))

                # if there is no next page, we're done.
                if 'paging' in statuses:
                    after = statuses['paging']['cursors']['after']
                else:
                    has_next_page = False
            if t_posts != 0:
                m_reaction = t_reaction // t_posts
                m_comments = t_comments // t_posts
            else:
                m_reaction = t_reaction
                m_comments = t_comments
            self.current_data['total_reactions'] = t_reaction
            self.current_data['total_comments'] = t_comments
            self.current_data['total_shares'] = t_shares
            self.current_data['total_posts'] = t_posts
            self.current_data['media_reactions'] = m_reaction
            self.current_data['media_comments'] = m_comments