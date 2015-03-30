# -*- coding: utf-8 -*-

import redis
from subredis import SubRedis
import pickle
import hashlib
import os

RECORD_EXPIRATION = 86400  # 1 day in seconds
REDIS_KEYSPACE = os.environ['REDIS_KEYSPACE']
REDIS_URL = os.environ['REDIS_URL']

conn = SubRedis(REDIS_KEYSPACE, redis.from_url(REDIS_URL))


def key_hash(k):
    return "bfc_" + hashlib.md5(k).hexdigest()


def exists(e):
    return conn.exists(key_hash(e.link))


def add_to_queue(e):
    return conn.lpush("bfc_queue", pickle.dumps(e))


def create_entry(e):
    conn.set(key_hash(e.link), True)
    return add_to_queue(e)


def get_next_to_run():
    return pickle.loads(conn.brpoplpush("bfc_queue", "bfc_runner"))


def remove_from_runner(e):
    return conn.lrem("bfc_runner", pickle.dumps(e)) > 0


def send_runner_to_queue(e):
    conn.brpoplpush("bfc_runner", "bfc_runner")
    ent = conn.brpoplpush("bfc_runner", "bfc_queue")
    return remove_from_runner(pickle.loads(ent))
