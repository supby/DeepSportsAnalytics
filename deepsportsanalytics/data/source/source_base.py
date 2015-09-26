# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from abc import ABCMeta
from abc import abstractmethod
import datetime
import logging
import datetime
import logging

logger = logging.getLogger(__name__)

class DataSourceFilter():

    def __init__(self, date_from, date_to, limit):
        if date_from:
            assert isinstance(date_from, datetime.date), \
                "date_from must be datetime.date"
        if date_to:
            assert isinstance(date_to, datetime.date), \
                "date_to must be datetime.date"

        self.dateFrom = date_from
        self.dateTo = date_to
        self.limit = limit
        
    def __str__(self):
        return "%s_%s_%s" % (str(self.dateFrom), 
                             str(self.dateTo), str(self.limit))


class DataSourceBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, filter):
        """load data from url"""
        assert isinstance(filter, DataSourceFilter), \
            "filter must be instance of DataSourceFilter class"


