import logging

from data.source.nhlreference_source import NHLRefDataSource
from shared.cache import DefaultCache

logger = logging.getLogger(__name__)

class DataSourceFactory(object):
    __ds_map = {
        'nhlref': lambda: NHLRefDataSource(team_stat_season=2015,
                                     games_season=2016,
                                     cache=DefaultCache.get_instance(),
                                     fvector_len=-1)
    }

    @staticmethod
    def create(data_source_type):
        logger.info('create: data_source_type = %s' % data_source_type)
        return DataSourceFactory.__ds_map.get(data_source_type, lambda: None)()
