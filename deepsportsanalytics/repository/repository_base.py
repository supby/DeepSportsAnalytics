from abc import ABCMeta
from abc import abstractmethod

class RepositoryBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, entity):
        """add entity to repo"""

    @abstractmethod
    def update(self, predicate, fields):
        """update entity to repo"""

    def get(self, predicate):
        """select data by predicate"""

    def delete(self, predicate):
        """delete data by predicate"""
