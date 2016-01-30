import sys
import datetime
from dateutil.parser import parse
import logging

from pymongo import MongoClient

from source_base import DataSourceBase

logger = logging.getLogger(__name__)

class MongoDBDataSource(DataSourceBase):

    def __init__(self, data_repo, collection_name, cache=None):
        self.__data_repo = data_repo
        self.__collection_name = collection_name
        self.__cache = cache

    def load(self, filter):
        logger.info('load')

        cache_key = '{0}_{1}'.format(self.__collection_name, str(filter))

        data = None
        if self.__cache:
            logger.info('trying to load from cache')
            data = self.__cache.get(cache_key)

        if not data:
            logger.info('load from source')
            f = {'meta.{0}'.format(k): filter[k] for k in filter.keys()}
            data = list(self.__data_repo.get(self.__collection_name, f))

            if self.__cache and data:
                self.__cache.set(cache_key, data)
        else:
            logger.info('loaded from cache')

        return data
