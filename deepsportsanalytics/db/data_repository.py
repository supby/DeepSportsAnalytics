import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)

class DataRepository(object):

    def __init__(self, url, db_name):
        self.__db = MongoClient(url)[db_name]

    def add(self, model_name, data):
        logger.info('add: model_name = %s' % model_name)
        self.__db['%s_data' % model_name].insert_many(data)

    def get(self, model_name, filter):
        logger.info('get: model_name = %s' % model_name)
        return self.__db['%s_data' % model_name].find(filter)
