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

class DataSourceBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, filter):
        """load data from url"""      
