from abc import ABCMeta
from abc import abstractmethod
import datetime
import logging

logger = logging.getLogger(__name__)


class ModelBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self):
        """update/retrain model with new data"""

    @abstractmethod
    def predict(self, X):
        """make prediction"""
