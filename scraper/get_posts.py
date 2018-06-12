import os
from time import strftime
import csv
import json


def process_posts(page, status, message, status_published):
    if not os.path.exists('json/posts/' + str(page)):
            os.makedirs('json/posts/' + str(page))
    post = pretty_post(status, message)
    post['published'] = status_published
    specific_comments = {}
    num_of_comment = 0
    for comment in status['comments']['data']:
        specific_comments['comment ' + str(num_of_comment)] = \
            comment['message']
        num_of_comment += 1
    post['specific_comments'] = specific_comments
    try:
        path = 'json/posts/' + str(page) + '/' + status['id'] + '.json'
        with open(path, 'w', encoding='utf8') as post_file:
            post_file.write(json.dumps(post, indent=2, ensure_ascii=False))
    except Exception as e:
        print('Algo errado na escrita do post' + str(e))


def pretty_post(status, message):
    post = {}
    post['id'] = status['id']
    post['message'] = '' if 'message' not in message.keys() else \
        message['message']
    post['link_to_post'] = '' if 'link' not in status else status['link']
    post['type'] = status['type']
    reactions = ['like', 'wow', 'sad', 'love', 'haha', 'angry']
    for react in reactions:
        post[react] = status[react]['summary']['total_count']
    post['story'] = message['story'] if 'story' in message.keys() else ''
    post['reactions'] = 0 if 'reactions' not in status.keys() else \
        status['reactions']['summary']['total_count']
    post['comments'] = 0 if 'comments' not in status else \
        status['comments']['summary']['total_count']
    post['shares'] = 0 if 'shares' not in status else status['shares']['count']
    return post


def write_posts_to_csv():
    path = 'json/posts'
    list_of_actors = os.listdir(path)
    columns = ['id', 'message', 'type', 'shares', 'published', 'story',
               'reactions', 'love', 'like', 'wow', 'sad', 'angry', 'haha',
               'link_to_post']
    time = strftime("%Y-%m-%d")
    if not os.path.exists('csv/' + time):
        os.makedirs('csv/' + time)
    try:
        for actor in list_of_actors:
            actor_file_name = 'csv/' + time + '/' + actor + '.csv'
            with open(actor_file_name, 'w', encoding='utf8') as csv_file:
                info = csv.writer(csv_file)
                info.writerow(columns)
                list_of_posts = os.listdir(path + '/' + actor)
                for post in list_of_posts:
                    list_of_content = []
                    json_post = path + '/' + actor + '/' + post
                    with open(json_post, 'r', encoding='utf8') as json_post:
                        content = json.load(json_post)
                        for key in columns:
                            list_of_content.append(content[key])
                    info.writerow(list_of_content)
    except Exception as e:
        print('Erro na escrita do csv: ' + str(e))


def write_comments_to_csv():
    path = 'json/posts'
    list_of_actors = os.listdir(path)
    time = strftime("%Y-%m-%d")
    for actor in list_of_actors:
        comt_file_name = 'csv/' + time + '/' + actor +\
            '_comments.csv'
        csv_comt_file = open(comt_file_name, 'w', encoding='utf8')
        comments_info = csv.writer(csv_comt_file)
        list_of_posts = os.listdir(path + '/' + actor)
        for post in list_of_posts:
            list_of_comments = []
            json_post = path + '/' + actor + '/' + post
            with open(json_post, 'r', encoding='utf8') as json_post:
                content = json.load(json_post)
                list_of_comments.append(content['id'])
                for comment in content['specific_comments'].items():
                    list_of_comments.append(comment)
            comments_info.writerow(list_of_comments)
        csv_comt_file.close()
