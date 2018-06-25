import os
from time import strftime
import csv
import json


def process_posts(page, status, message, status_published):
    post = pretty_post(status, message)
    post = get_reactions_info(post, status, message)
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
    post['type'] = status['type']
    post['message'] = '' if 'message' not in message.keys() else \
        message['message']
    post['link_to_post'] = '' if 'link' not in status else \
        status['link']
    return post


def get_reactions_info(post, status, message):
    post['story'] = message['story'] if 'story' in message.keys() else ''
    reactions = ['like', 'wow', 'sad', 'love', 'haha', 'angry',
                 'reactions', 'comments']
    for react in reactions:
        post[react] = status[react]['summary']['total_count']
    return post


def write_posts_to_csv():
    path = 'json/posts'
    columns = ['id', 'message', 'type', 'published', 'story',
               'reactions', 'love', 'like', 'wow', 'sad', 'angry',
               'haha', 'link_to_post']
    list_of_actors = os.listdir(path)
    time = strftime("%Y-%m-%d")
    for actor in list_of_actors:
        list_of_content = []
        list_of_posts = os.listdir(path + '/' + actor)
        for post in list_of_posts:
            json_post = path + '/' + actor + '/' + post
            with open(json_post, 'r', encoding='utf8') as json_post:
                content = json.load(json_post)
            list_of_content.append(get_info(content, columns))
        actor_file_name = 'csv/' + time + '/' + actor + '.csv'
        dump_to_csv(actor_file_name, list_of_content, columns)


def dump_to_csv(path, list_of_content, columns):
    with open(path, 'w', encoding='utf8') as csv_file:
        info = csv.writer(csv_file)
        info.writerow(columns)
        for row in list_of_content:
            info.writerow(row)


def get_info(content, keys):
    list_of_content = []
    for key in keys:
        list_of_content.append(content[key])
    return list_of_content


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
                list_of_comments = dict_to_list(
                    content['specific_comments'], list_of_comments)
            comments_info.writerow(list_of_comments)
        csv_comt_file.close()


def dict_to_list(dictionary, list_of_comments):
    for comment in dictionary.values():
        list_of_comments.append(comment)
    return list_of_comments
