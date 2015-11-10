import sys
import datetime
from dateutil.parser import parse
import logging

from pymongo import MongoClient

from source_base import DataSourceBase

logger = logging.getLogger(__name__)

class MongoDBDataSource(DataSourceBase):

    def __init__(self, url, model_name, db_name):
        self.__db = MongoClient(url)[db_name]
        self.__model_name = model_name

    def load(self, filter):
        logger.info('load')
        for row in self.__db['%s_data' % self.__model_name].find(filter):
            yield return row
