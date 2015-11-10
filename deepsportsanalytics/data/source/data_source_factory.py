import logging

from data.source.nhlreference_source import NHLRefDataSource
from shared.cache import DefaultCache
from shared.redis_cache import RedisCache

logger = logging.getLogger(__name__)

class DataSourceFactory(object):
    __ds_map = {
        'nhlref': lambda c: NHLRefDataSource(team_stat_season=2015,
                                     games_season=2016,
                                     cache=RedisCache(url=c['REDIS_URL']),
                                     fvector_len=-1)
    }

    def __init__(self, config):
        self.__config = config

    def create(self, data_source_type):
        logger.info('create: data_source_type = %s' % data_source_type)
        return DataSourceFactory.__ds_map.get(data_source_type, lambda c: None)(self.__config)
