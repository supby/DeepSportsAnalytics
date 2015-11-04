import logging
import pickle

from azure.storage import BlobService

from storage_base import StorageBase

logger = logging.getLogger(__name__)

class AzureBlobStorage(StorageBase):

    def __init__(self, account_name, account_key, container_name):
        self.__container_name = container_name
        self.__blob_service = BlobService(account_name=account_name,
                                          account_key=account_key)
        self.__blob_service.create_container(container_name)

    def get(self, key, default=None):
        logger.info('get: key = %s' % key)
        return pickle.loads(self.__blob_service
                            .get_blob_to_text(self.__container_name, key))

    def set(self, key, value):
        logger.info('get: key = %s, value = %s' % (key, value))
        self.__blob_service.put_block_blob_from_text(self.__container_name,
                                                     key, pickle.dumps(value))
