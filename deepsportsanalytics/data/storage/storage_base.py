# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Andre_Suzanovich"
__date__ = "$Jun 16, 2015 12:00:44 PM$"

from abc import ABCMeta
from abc import abstractmethod

class StorageBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, key, default):
        """get valur from storage"""
        pass

    @abstractmethod
    def set(self, key, value):
        """set value in storage"""
        pass
