import sys
import datetime
from dateutil.parser import parse
import logging

from source_base import DataSourceBase
from shared.cache import CacheBase

logger = logging.getLogger(__name__)

class AzureDataSource(DataSourceBase):

    def __init__(self, source_name, data_storage):
        self.__data_storage = data_storage
        self.__source_name = source_name

    def load(self, filter):
        data = self.__data_storage.get(self.__source_name)      
