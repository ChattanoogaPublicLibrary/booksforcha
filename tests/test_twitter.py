# -*- coding: utf-8 -*-

"""Tests for booksforcha"""

import unittest
import nose
import booksforcha.twitter as twitter


class TestTwitter(unittest.TestCase):

    def test_message(self):
        msg = twitter.message(
            'Some Book - Sean Brewer', 'http://www.example.com/4')
        self.assertEqual(
            msg, 'Some Book - Sean Brewer http://www.example.com/4')

    def test_send_tweet(self):
        self.assertFalse(twitter.send_tweet('title and author', 'url'))


if __name__ == '__main__':
    nose.run()
