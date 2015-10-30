import global_config
from data.source.nhlreference_source import NHLRefDataSource
from shared.cache import DefaultCache

class DataSourceFactory(object):
    __ds_map = {
        'nhlref': NHLRefDataSource(team_stat_season=2015,
                                     games_season=2016,
                                     cache=DefaultCache.get_instance(),
                                     fvector_len=-1)
    }

    @staticmethod
    def create(data_source_type):
        return __ds_map.get(data_source_type, None)
