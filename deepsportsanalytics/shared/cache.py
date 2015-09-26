# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "andrej"
__date__ = "$Apr 7, 2015 9:42:17 PM$"

from abc import ABCMeta
from abc import abstractmethod
import logging
import threading
logger = logging.getLogger(__name__)

class CacheBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, key):
        """get cached item if it exists"""
        pass

    @abstractmethod
    def set(self, key, val):
        """cache item"""
        pass

    @abstractmethod
    def contains(self, key):
        """check if item is in cache"""
        pass


class DefaultCache(CacheBase):

    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        """init in memory dict cache"""
        self.__cache = {}

    @staticmethod
    def get_instance():
        """get singlton instance"""
        DefaultCache.__lock.acquire()
        if not DefaultCache.__instance:
            DefaultCache.__instance = DefaultCache()
        DefaultCache.__lock.release()

        return DefaultCache.__instance

    def get(self, key):
        """use in-memory for getting values by key"""
        logger.info("DefaultCache -> [get], key:%s" % str(key))
        return self.__cache.get(key, None)

    def set(self, key, val):
        """set value in memory cache"""
        logger.info("DefaultCache -> [set], key:%s" % str(key))
        self.__cache[key] = val

    def contains(self, key):
        """check if item is in dict mem cache"""
        has_key = key in self.__cache
        logger.info("DefaultCache -> [contains] key: %s, exists: %s" % (str(key), str(has_key)))
        return has_key
