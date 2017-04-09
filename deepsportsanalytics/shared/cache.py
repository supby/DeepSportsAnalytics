from abc import ABCMeta
from abc import abstractmethod
import logging
import threading
logger = logging.getLogger(__name__)


class DefaultCache(object):

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
