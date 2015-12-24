import sys
import datetime
from dateutil.parser import parse
import logging

from pymongo import MongoClient

from source_base import DataSourceBase

logger = logging.getLogger(__name__)

class MongoDBDataSource(DataSourceBase):

    def __init__(self, data_repo, collection_name):
        self.__data_repo = data_repo
	self.__collection_name = collection_name

    def load(self, filter):
        logger.info('load')

        f = {'meta.{0}'.format(k): filter[k] for k in filter.keys()}
        return self.__data_repo.get(self.__collection_name, f)
