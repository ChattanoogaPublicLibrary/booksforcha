# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from feed import load_feed
from twitter import send_queued_tweet
import os


RSS_FEED_LIST = os.environ['RSS_FEED_LIST']
LOAD_FEED_SECONDS = int(os.environ['LOAD_FEED_SECONDS'])
SEND_QUEUED_TWEET_SECONDS = int(os.environ['SEND_QUEUED_TWEET_SECONDS'])

sched = BlockingScheduler()


def parse_feed_list(s):
    parsed = s.split(',')

    if parsed == ['']:
        return []
    else:
        return parsed


@sched.scheduled_job('interval', seconds=LOAD_FEED_SECONDS)
def feed_loader():
    load_feed(parse_feed_list(RSS_FEED_LIST))


@sched.scheduled_job('interval', seconds=SEND_QUEUED_TWEET_SECONDS)
def tweet():
    send_queued_tweet()


def main():
    sched.start()


def __main__():
    main()


if __name__ == "__main__":
    try:
        __main__()
    except (KeyboardInterrupt):
        exit('Received Ctrl+C. Stopping application.', 1)
