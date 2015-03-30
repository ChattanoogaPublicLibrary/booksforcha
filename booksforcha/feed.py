# -*- coding: utf-8 -*-

import feedparser
import entry


def compile_feeds(rsslist):
    return reduce(lambda i, j: i + j,
                  map(lambda k: feedparser.parse(k)['entries'], rsslist), [])


def load_feed(rsslist):
    for i in compile_feeds(rsslist):
        if not entry.exists(i):
            entry.create_entry(i)
