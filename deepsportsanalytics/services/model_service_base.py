from abc import ABCMeta
from abc import abstractmethod
import datetime
import logging

logger = logging.getLogger(__name__)

class ModelServiceBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, date_from, date_to):
        """update/retrain model with new data"""
        assert isinstance(date_from, datetime.datetime.date), \
            "datepredict have to be datetime.datetime.date type"
        assert isinstance(date_to, datetime.datetime.date), \
            "datepredict have to be datetime.datetime.date type"

    @abstractmethod
    def predict(self, datepredict):
        """make prediction"""
        assert isinstance(datepredict, datetime.datetime.date), \
            "datepredict have to be datetime.datetime.date type"

    @abstractmethod
    def status(self):
        """get status of processing"""
