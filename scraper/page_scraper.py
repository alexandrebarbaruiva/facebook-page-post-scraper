import os
import json
import csv
import datetime
from time import strftime
import requests
import facebook

from pathlib import Path
home = Path.home()


class Scraper:
    """
    Scraper responsible for collecting posts from Facebook
    """
    def __init__(self, token):
        self.token = token
        self.status_code = 400
        self.current_data = ''
        self.csv_dir = home.joinpath('csv')
        self.json_dir = home.joinpath('json')
        if not self.csv_dir.is_dir():
            self.csv_dir.mkdir()
        if not self.json_dir.is_dir():
            self.json_dir.mkdir()

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

    def valid_page(self, page=None):
        if page is None:
            page = self.page
        valid_url = 'https://www.facebook.com/' + str(page)
        valid_status_code = requests.get(valid_url).status_code
        return(valid_status_code == 200)

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
            print(inst)
            return 'Page not defined or bad query structure'

    def write_file(self, file=None):
        if file is None:
            file = self.file_name
        with open(str(self.json_dir.joinpath(file)), 'w', encoding='utf8') \
                as data_file:
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
            if set(column_names) == {
                    'name', 'id', 'date', 'fan_count', 'total_posts',
                    'total_reactions', 'total_comments', 'total_shares',
                    'average_reactions', 'average_comments'
            }:
                column_names = [
                    'name', 'id', 'date', 'fan_count', 'total_posts',
                    'total_reactions', 'total_comments', 'total_shares',
                    'average_reactions', 'average_comments'
                ]
            elif set(column_names) == {'name', 'id', 'date', 'fan_count'}:
                column_names = ['name', 'id', 'date', 'fan_count']
        except Exception as inst:
            print(inst)
            return 'No content found.'
        today = strftime("%Y-%m-%d_%Hh")

        # Check if file already exists to append instead of create
        csv_file = self.csv_dir.joinpath('{}_{}.csv'.format(file_name, today))
        if csv_file.exists():
            content = dict_to_list()
            # Check if content already exists in csv
            with open(
                    str(csv_file), 'r') as csvfile:
                reader = csv.reader(csvfile)
                reader_list = list(reader)
                for row in reader_list:
                    if row == content:
                        return True
            # Write content on CSV because it's not duplicated
            with open(
                    str(csv_file), 'a') as csvfile:
                info = csv.writer(csvfile)
                info.writerow(content)
            return True

        # Create file because file doesn't exist
        with open(str(csv_file), 'w') as csvfile:
            info = csv.writer(csvfile)
            content = dict_to_list()
            info.writerow(column_names)
            info.writerow(content)
        return True

    def processFacebookPageFeedStatus(
        self, status, total_reaction, total_comments, total_shares
    ):

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
            '%Y-%m-%d %H:%M:%S')  # Converting from the way facebook gives us
        # the created time to a more readable

        # Nested items require chaining dictionary keys.

        num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
        num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status else status['shares']['count']
        total_reaction = total_reaction + num_reactions
        total_comments = total_comments + num_comments
        total_shares = total_shares + num_shares

        return status_id, status_published, num_reactions, num_comments, \
            num_shares, total_reaction, total_comments, total_shares

    def get_reactions(self, page=None, since_date=None, until_date=None):
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        if page is None:
            page = self.page
        if not self.valid_page(page):
            return "Page is not valid."
        if since_date is None:
            month = str(int(strftime("%m"))-1)
            since_date = strftime("%Y-") + month + strftime("-%d")
        if until_date is None:
            until_date = strftime("%Y-%m-%d")
        total_reaction = 0
        total_comments = 0
        total_shares = 0
        total_posts = 0
        has_next_page = True
        num_processed = 0
        after = ''
        since = "&since={}".format(since_date) if since_date \
            != '' else ''
        until = "&until={}".format(until_date) if until_date \
            != '' else ''
        while has_next_page:
            after = '' if after == '' else "&after={}".format(after)
            fields = "fields=message,created_time,type,id," + \
                "comments.limit(0).summary(true),shares,reactions" + \
                ".limit(0).summary(true)"

            statuses = graph.get_object(
                id=str(self.page)+'/posts?'+after+'&limit=100'+since+until,
                fields=fields
            )
            for status in statuses['data']:
                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = self.processFacebookPageFeedStatus(
                        status, total_reaction, total_comments, total_shares
                    )
                    total_reaction = status_data[5]
                    total_comments = status_data[6]
                    total_shares = status_data[7]
                    total_posts += 1
                num_processed += 1
                if num_processed % 100 == 0:
                    print(
                        "{} Statuses Processed: {}".format(
                            num_processed, datetime.datetime.now()
                        )
                    )
            # if there is no next page, we're done.
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
            else:
                has_next_page = False
        if total_posts != 0:
            average_reaction = total_reaction // total_posts
            average_comments = total_comments // total_posts
        else:
            average_reaction = total_reaction
            average_comments = total_comments
        self.current_data['total_reactions'] = total_reaction
        self.current_data['total_comments'] = total_comments
        self.current_data['total_shares'] = total_shares
        self.current_data['total_posts'] = total_posts
        self.current_data['average_reactions'] = average_reaction
        self.current_data['average_comments'] = average_comments
