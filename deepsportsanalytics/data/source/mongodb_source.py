import sys
import datetime
from dateutil.parser import parse
import logging

from pymongo import MongoClient

from source_base import DataSourceBase

logger = logging.getLogger(__name__)

class MongoDBDataSource(DataSourceBase):

    def __init__(self, data_repo):
        self.__data_repo = data_repo

    def load(self, model_name, filter):
        logger.info('load')
        self.__data_repo.get(model_name, filter)
