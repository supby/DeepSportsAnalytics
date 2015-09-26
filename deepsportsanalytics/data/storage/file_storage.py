# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import pickle

from storage_base import StorageBase

class FileStorage(StorageBase):

    def __init__(self, storage_filename):
        self.storage_filename = storage_filename
        if not os.path.exists(self.storage_filename):
            pickle.dump(dict(), open(self.storage_filename, 'wb'))

    def get(self, key, default=None):
        return pickle.load(open(self.storage_filename, 'rb')).get(key, default)

    def set(self, key, value):
        storage_dict = pickle.load(open(self.storage_filename, 'rb'))
        storage_dict[key] = value
        pickle.dump(storage_dict, open(self.storage_filename, 'wb'))


