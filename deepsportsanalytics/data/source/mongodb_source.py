import sys
import datetime
from dateutil.parser import parse
import logging

from pymongo import MongoClient

from source_base import DataSourceBase

logger = logging.getLogger(__name__)

class MongoDBDataSource(DataSourceBase):

    def __init__(self, data_repo, source_name):
        self.__data_repo = data_repo
	self.__source_name = source_name

    def load(self, filter):
        logger.info('load')
        self.__data_repo.get(self.__source_name, filter)
