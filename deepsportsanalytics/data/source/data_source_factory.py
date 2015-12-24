import logging

from data.source.nhlreference_source import NHLRefDataSource
from shared.cache import DefaultCache
from shared.redis_cache import RedisCache
from data.storage.data_repository import DataRepository
from data.source.mongodb_source import MongoDBDataSource

logger = logging.getLogger(__name__)

class DataSourceFactory(object):
    __ds_map = {
                'nhlref_2015_2016': lambda c:
                    MongoDBDataSource(
                        data_repo=DataRepository(uri=c['MONGO_URI']),
					    collection_name='nhlref_2015_2016'),
                'nhlref_all': lambda c:
                    MongoDBDataSource(
                        data_repo=DataRepository(uri=c['MONGO_URI']),
					    collection_name='nhlref_all')
    }

    def __init__(self, config):
        self.__config = config

    def create(self, data_source_type):
        logger.info('create: data_source_type = %s' % data_source_type)
        return DataSourceFactory.__ds_map.get(data_source_type, lambda c: None)(self.__config)
