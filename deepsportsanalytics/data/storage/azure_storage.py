# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pickle
from azure.storage import BlobService

from storage_base import StorageBase

class AzureBlobStorage(StorageBase):

    def __init__(self, account_name, account_key, container_name):
        self.__container_name = container_name
        self.__blob_service = BlobService(account_name=account_name, 
                                          account_key=account_key)
        self.__blob_service.create_container(container_name)

    def get(self, key, default=None):
        return pickle.loads(self.__blob_service
                            .get_blob_to_text(self.__container_name, key))

    def set(self, key, value):
        self.__blob_service.put_block_blob_from_text(self.__container_name, 
                                                     key, pickle.dumps(value))




