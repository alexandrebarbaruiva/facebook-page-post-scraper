import json
import datetime
import csv
import time
from time import strftime
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

page_id = "419702371406944"

# input date formatted as YYYY-MM-DD
since_date = "2018-04-20"
until_date = strftime("%Y-%m-%d")

access_token = ""



def request_until_succeed(url):
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

def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=message,created_time,type,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true)"

    return base_url + fields


def processFacebookPageFeedStatus(status,t_reaction,t_comments,t_shares):

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


def scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date):
    with open(strftime("%Y-%m-%d--%H-%M.csv"), 'w') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_published", "num_reactions",
                    "num_comments", "num_shares","total reaction","total comments","total shares"])
        t_reaction = 0
        t_comments = 0
        t_shares = 0
        has_next_page = True
        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        after = ''
        base = "https://graph.facebook.com/v2.12"
        node = "/{}/posts".format(page_id)
        parameters = "/?limit={}&access_token={}".format(100, access_token)
        since = "&since={}".format(since_date) if since_date \
            is not '' else ''
        until = "&until={}".format(until_date) if until_date \
            is not '' else ''

        print("Scraping {} Facebook Page: {}\n".format(page_id, scrape_starttime))

        while has_next_page:
            after = '' if after is '' else "&after={}".format(after)
            base_url = base + node + parameters + after + since + until

            url = getFacebookPageFeedUrl(base_url)
            statuses = json.loads(request_until_succeed(url))

            for status in statuses['data']:

                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = processFacebookPageFeedStatus(status,t_reaction,t_comments,t_shares)
                    t_reaction = status_data[5]
                    t_comments = status_data[6]
                    t_shares =  status_data[7]
                    w.writerow(status_data)

                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Statuses Processed: {}".format
                          (num_processed, datetime.datetime.now()))

            # if there is no next page, we're done.
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
            else:
                has_next_page = False
        w.writerow(["total de posts","total reactions","total comentarios","total shares"])
        w.writerow([num_processed,t_reaction,t_comments,t_shares])
        print("\nDone!\n{} Statuses Processed in {}".format(
              num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date)
