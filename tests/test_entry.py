"""Tests for entry"""

import unittest
import nose
import os
import pickle
import redis
from subredis import SubRedis
import booksforcha.entry as entry
import booksforcha.feed as feed

MODULE_PATH = os.path.dirname(__file__) + '/fixtures/'
REDIS_KEYSPACE = 'BFC_TEST'
REDIS_URL = 'redis://localhost:6379'


class TestEntry(unittest.TestCase):

    def setUp(self):
        records = feed.compile_feeds([MODULE_PATH + 'feed.xml'])
        self.conn = SubRedis(REDIS_KEYSPACE,
                             redis.from_url(REDIS_URL))
        self.fake_xml_record = records[0]
        self.all_fake_xml_records = records

    def tearDown(self):
        self.conn.flushdb()

    def test_key_hash(self):
        hsh = entry.key_hash('http://www.chattlibrary.org')
        self.assertEqual('bfc_f746128de6c136fe5977ab8c746202d4', hsh)

    def test_exists(self):
        entry.create_entry(self.fake_xml_record)

        does_exist = entry.exists(self.fake_xml_record)

        self.assertTrue(does_exist)

    def test_create_entry(self):
        entry.create_entry(self.fake_xml_record)

        self.assertTrue(entry.exists(self.fake_xml_record))

        self.assertTrue(self.conn.llen("bfc_queue"), 1)

    def test_create_success(self):
        e = entry.create_entry(self.fake_xml_record)

        self.assertTrue(e)

    def test_add_to_queue(self):
        entry.add_to_queue(self.all_fake_xml_records[0])
        entry.add_to_queue(self.all_fake_xml_records[1])

        self.assertEqual(self.conn.llen("bfc_queue"), 2)

    def test_get_next_to_run(self):
        entry.add_to_queue(self.all_fake_xml_records[0])
        entry.add_to_queue(self.all_fake_xml_records[1])

        a = entry.get_next_to_run()
        b = entry.get_next_to_run()

        self.assertEqual(a.title, "This Is A Cool Test Book And Stuff")
        self.assertEqual(b.title, "Another Test Title For Some Book")

    def test_remove_from_runner(self):
        entry.add_to_queue(self.all_fake_xml_records[0])
        entry.add_to_queue(self.all_fake_xml_records[1])

        a = entry.get_next_to_run()

        entry.remove_from_runner(a)

        self.assertEqual(self.conn.llen("bfc_queue"), True)

        entry.get_next_to_run()

        self.assertEqual(self.conn.llen("bfc_queue"), False)

    def test_send_runner_to_queue(self):
        entry.add_to_queue(self.all_fake_xml_records[0])
        entry.add_to_queue(self.all_fake_xml_records[1])

        a = entry.get_next_to_run()
        b = entry.get_next_to_run()

        entry.send_runner_to_queue(b)

        self.assertEqual(self.conn.llen('bfc_queue'), 1)
        self.assertEqual(self.conn.llen('bfc_runner'), 1)

        self.assertEqual(pickle.loads(self.conn.lpop('bfc_queue')), b)
        self.assertEqual(pickle.loads(self.conn.lpop('bfc_runner')), a)

if __name__ == '__main__':
    nose.run()
