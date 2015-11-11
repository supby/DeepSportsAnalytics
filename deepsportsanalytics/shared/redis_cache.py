from abc import ABCMeta
from abc import abstractmethod
import logging
import threading
import pickle

import redis

logger = logging.getLogger(__name__)

class RedisCache(object):

    def __init__(self, url):
        self.__r = redis.from_url(url)

    def get(self, key):
        logger.info("RedisCache -> [get], key:%s" % str(key))
        pickled_value = self.__r.get(key)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def set(self, key, val):
        logger.info("RedisCache -> [set], key:%s" % str(key))
        self.__r.set(key, pickle.dumps(val))
