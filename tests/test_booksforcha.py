"""Tests for booksforcha"""

import unittest
import nose
import os
import booksforcha.booksforcha as booksforcha

MODULE_PATH = os.path.dirname(__file__) + '/fixtures/'


class TestBooksforcha(unittest.TestCase):

    def test_parse_feed_list(self):
        s1 = ''
        self.assertEqual(booksforcha.parse_feed_list(s1), [])

        s2 = 'http://www.example.com,http://example.example.com'
        self.assertEqual(booksforcha.parse_feed_list(s2),
                         ['http://www.example.com',
                         'http://example.example.com'])

        s3 = 'http://www.example.com'
        self.assertEqual(booksforcha.parse_feed_list(s3),
                         ['http://www.example.com'])

if __name__ == '__main__':
    nose.run()
