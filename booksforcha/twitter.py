# -*- coding: utf-8 -*-

import tweepy
import os
from entry import get_next_to_run, remove_from_runner, send_runner_to_queue

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


def message(info, url):
    return (info + ' ' + url).encode('utf-8')


def send_tweet(info, url):
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        api.update_status(status=message(info, url))

        return True
    except tweepy.error.TweepError:
        return False


def send_queued_tweet():
    next_entry = get_next_to_run()

    if send_tweet(next_entry.title, next_entry.link):
        return remove_from_runner(next_entry)
    else:
        send_runner_to_queue(next_entry)
        return False
