# -*- coding: utf-8 -*-

import schedule
from feed import load_feed
from twitter import send_queued_tweet
import time
import os


RSS_FEED_LIST = os.environ['RSS_FEED_LIST']
LOAD_FEED_SECONDS = int(os.environ['LOAD_FEED_SECONDS'])
SEND_QUEUED_TWEET_SECONDS = int(os.environ['SEND_QUEUED_TWEET_SECONDS'])


def parse_feed_list(s):
    parsed = s.split(',')

    if parsed == ['']:
        return []
    else:
        return parsed


def main():
    rsslist = parse_feed_list(RSS_FEED_LIST)
    schedule.every(LOAD_FEED_SECONDS).seconds.do(load_feed, rsslist)
    schedule.every(SEND_QUEUED_TWEET_SECONDS).seconds.do(send_queued_tweet)

    while True:
        schedule.run_pending()
        time.sleep(1)


def __main__():
    main()


if __name__ == "__main__":
    try:
        __main__()
    except (KeyboardInterrupt):
        exit('Received Ctrl+C. Stopping application.', 1)
