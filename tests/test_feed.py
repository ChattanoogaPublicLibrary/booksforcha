"""Tests for feed"""

import unittest
import nose
import os
import redis
from subredis import SubRedis
import booksforcha.feed as feed

MODULE_PATH = os.path.dirname(__file__) + '/fixtures/'
REDIS_KEYSPACE = 'BFC_TEST'
REDIS_URL = 'redis://localhost:6379'


class TestFeed(unittest.TestCase):

    def setUp(self):
        self.records = feed.compile_feeds([MODULE_PATH + 'feed.xml'])
        self.conn = SubRedis(REDIS_KEYSPACE,
                             redis.from_url(REDIS_URL))
        self.rss_urls = [MODULE_PATH + 'feed.xml']

    def tearDown(self):
        self.conn.flushdb()

    def test_compile_feeds(self):
        self.assertEqual(len(self.records), 2)

    def test_compile_feeds_empty(self):
        self.assertEqual(len(feed.compile_feeds([])), 0)

    def test_compile_feeds_multiple(self):
        feeds = feed.compile_feeds(
            [MODULE_PATH + 'feed.xml', MODULE_PATH + 'feed2.xml'])
        self.assertEqual(len(feeds), 4)

    def test_load_feed(self):
        feed.load_feed(self.rss_urls)

        self.assertEqual(self.conn.llen("bfc_queue"), 2)

        # If we try to load them again, they shouldn't
        # be added to the queue.
        feed.load_feed(self.rss_urls)

        self.assertEqual(self.conn.llen("bfc_queue"), 2)

if __name__ == '__main__':
    nose.run()
