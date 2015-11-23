import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)

class DataRepository(object):

    def __init__(self, uri):
        self.__db = MongoClient(uri).get_default_database()

    def add(self, collection_name, data):
        logger.info('add: collection_name = %s' % collection_name)
        self.__db[collection_name].insert_many(data)

    def get(self, collection_name, filter):
        logger.info('get: collection_name = %s' % collection_name)
        
        for r in self.__db[collection_name].find(filter):
            yield r
