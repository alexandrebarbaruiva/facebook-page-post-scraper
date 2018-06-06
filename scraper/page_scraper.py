import os
import json
import csv
import datetime
from time import strftime
import requests
import facebook


class Scraper:
    """
    Scraper responsible for collecting posts from Facebook
    """
    def __init__(self, token):
        self.token = token
        self.status_code = 400
        self.current_data = ''
        self.file_name = None
        self.actors_list = []
        self.date_list = []
        if not os.path.exists('csv/'):
            os.makedirs('csv/')
        if not os.path.exists('json/posts'):
            os.makedirs('json/posts')

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
        self.file_name = (str(self.page))

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
                id=str(self.page) + feed_statement,
                fields=query
            )
            self.current_data = post
            self.current_data['date'] = strftime("%Y-%m-%d")
            # print(self.current_data)
            if 'name' in post.keys():
                return post['name']
            elif 'data' in post.keys():
                return True
        except Exception as inst:
            print(inst)
            return 'Page not defined or bad query structure'

    def write_to_json(self, actor_name=None, file=None):
        if file is None:
            file = self.file_name
        with open('json/' + strftime("%Y-%m-%d") + '/' + file + '.json',
                  'w', encoding='utf8') as data_file:
                data_file.write(
                    json.dumps(self.current_data, indent=2, ensure_ascii=False)
                )  # pretty json
        if actor_name is not None:
            self.actors_list.append(actor_name)
        return True

    def get_page_name_and_like(self, page=None):
        self.scrape_current_page(page, query='name,fan_count')
        return([
            self.current_data['name'],
            # self.current_data['fan_count'],
            # self.current_data['id'],
            strftime("%Y-%m-%d")
        ])

    def write_to_csv(self, file_name='scraped'):
        def dict_to_list():
            content = []
            for column in column_names:
                content.append(str(self.current_data[column]))
            return content
        try:
            column_names = self.current_data.keys()
            if set(column_names) == {
                'name', 'id', 'date', 'since_date', 'until_date',
                'fan_count', 'total_posts', 'total_reactions',
                'total_comments', 'total_shares', 'average_reactions',
                'average_comments'
            }:
                column_names = [
                    'name', 'id', 'date', 'since_date', 'until_date',
                    'fan_count', 'total_posts', 'total_reactions',
                    'total_comments', 'total_shares', 'average_reactions',
                    'average_comments'
                ]
            elif set(column_names) == {
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

    def processFacebookPageFeedStatus(
        self, status, total_reaction, total_comments, total_shares, page, message
    ):

        # The status is now a Python dictionary, so for top-level items,
        # we can simply call the key.

        # Additionally, some items may not always exist,
        # so must check for existence first

        # Time needs special care since a) it's in UTC and
        # b) it's not easy to use in statistical programs.
        post={}
        if not os.path.exists('json/posts/'+str(self.page)):
            os.makedirs('json/posts/'+str(self.page))

        status_id = status['id']

        status_published = datetime.datetime.strptime(
            status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
        status_published = status_published + \
            datetime.timedelta(hours=-3)  # Brasilia time
        status_published = status_published.strftime(
            '%Y-%m-%d %H:%M:%S')
        post['id'] = status_id
        post['message'] = '' if 'message' not in message.keys() else message['message']
        post['published'] = status_published
        post['link_to_post'] = '' if 'link' not in status.keys() else status['link']
        post['type'] = status['type']
        post['like'] = status['like']['summary']['total_count']
        post['wow'] = status['wow']['summary']['total_count']
        post['sad'] = status['sad']['summary']['total_count']
        post['love'] = status['love']['summary']['total_count']
        post['haha'] = status['haha']['summary']['total_count']
        post['angry'] = status['angry']['summary']['total_count']
        post['story'] = message['story'] if 'story' in message.keys() else ''
        # Converting from the way facebook gives us
        # the created time to a more readable

        # Nested items require chaining dictionary keys.

        num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
        post['reactions'] = num_reactions
        num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
        post['comments'] = num_comments
        specific_comments = {}
        num_of_comment = 0
        for comment in status['comments']['data']:
            specific_comments['comment '+str(num_of_comment)]=comment['message']
            num_of_comment+=1
        post['specific_comments'] = specific_comments
        num_shares = 0 if 'shares' not in status else status['shares']['count']
        post['shares'] = num_shares
        if not os.path.exists('json/posts/'+str(self.page)):
            os.makedirs('json/posts/'+str(self.page))
        try:
            with open('json/posts/'+str(self.page)+'/'+status_id+'.json','w') as post_file:
                post_file.write(json.dumps(post, indent=2, ensure_ascii=False))
        except Exception as e:
            print(e)
            print('Algo errado na escrita do post')
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
            month = str(int(strftime("%m")) - 1)
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
                     "comments.limit(100).summary(total_count),shares,reactions" + \
                     ".limit(0).summary(true),link,reactions.type(LIKE).limit(0)" + \
                     ".summary(total_count).as(like),reactions.type(WOW).limit(0)" + \
                     ".summary(total_count).as(wow),reactions.type(SAD).limit(0).summary(total_count).as(sad)" + \
                     ",reactions.type(LOVE).limit(0).summary(total_count).as(love)," + \
                     "reactions.type(HAHA).limit(0).summary(total_count).as(haha)," + \
                     "reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"

            statuses = graph.get_object(
                id=str(self.page) + '/posts?' + after +
                '&limit=100' + since + until,
                fields=fields
            )
            for status in statuses['data']:
                post_message = graph.get_object(
                    id=status['id'],
                    fields="message,story"
                )
                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = self.processFacebookPageFeedStatus(
                        status, total_reaction, total_comments, total_shares, page, post_message
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
        self.current_data['since_date'] = since_date
        self.current_data['until_date'] = until_date
        self.current_data['total_reactions'] = total_reaction
        self.current_data['total_comments'] = total_comments
        self.current_data['total_shares'] = total_shares
        self.current_data['total_posts'] = total_posts
        self.current_data['average_reactions'] = average_reaction
        self.current_data['average_comments'] = average_comments

    def write_posts_to_csv(self):
        path = 'json/posts'
        list_of_actors = os.listdir(path)
        columns = ['id','message','type','shares','published','story','reactions',
                   'love','like','wow','sad','angry','haha','link_to_post']
        time = strftime("%Y-%m-%d")
        try:
            for actor in list_of_actors:
                with open('csv/'+actor+time+'.csv','w') as csv_file:
                    csv_comments_file = open('csv/'+actor+time+'_comments.csv','w')
                    comments_info = csv.writer(csv_comments_file)
                    info = csv.writer(csv_file)
                    info.writerow(columns)
                    list_of_posts = os.listdir(path+'/'+actor)
                    for post in list_of_posts:
                        list_of_content = []
                        list_of_comments = []
                        with open(path+'/'+actor+'/'+post,'r',encoding = 'utf8') as json_post:
                            content = json.load(json_post)
                            list_of_comments.append(content['id'])
                            for comment in content['specific_comments']:
                                list_of_comments.append(content['specific_comments'][comment])
                            for key in columns:
                                list_of_content.append(content[key])
                        comments_info.writerow(list_of_comments)
                        info.writerow(list_of_content)
                    csv_comments_file.close()
        except Exception as e:
            print('Erro na escrita do csv: '+str(e))
            
    def write_actors_and_date_file(self):
        data = {'date': [], 'latest': strftime("%Y-%m-%d")}
        actors_dict = {'actors': self.actors_list}
        with open('json/' + 'actors.json', 'w', encoding='utf8') as actor_file:
            actor_file.write(
                json.dumps(actors_dict, indent=2, ensure_ascii=False)
            )
        try:
            date_file = open('json/date.json', 'r+', encoding='utf8')
            data = json.load(date_file)
            data['latest'] = strftime("%Y-%m-%d")
            # print(data)
            date_file.seek(0)
            if strftime("%Y-%m-%d") not in data['date']:
                data['date'].append(strftime("%Y-%m-%d"))
                # print(data)
            date_file.write(
                json.dumps(data, indent=2, ensure_ascii=False)
            )
        except FileNotFoundError:
            data['date'].append(strftime("%Y-%m-%d"))
            data['latest'] = strftime("%Y-%m-%d")
            with open('json/date.json', 'w', encoding='utf8') as date_file:
                date_file.write(
                    json.dumps(data, indent=2, ensure_ascii=False)
                )
