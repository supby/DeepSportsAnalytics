import os
import sys
import logging
import logging.config
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import global_config
from data.storage.azure_storage import AzureBlobStorage
from shared.cache import DefaultCache
from data.source.source_base import DataSourceFilter
from data.source.nhlreference_source import NHLRefDataSource
from services.model_service_azure import AzureModelService
from utils import date_utils
from utils.thread_utils import AsyncMethod

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(process)d:%(thread)d] \
                                [%(levelname)s] [%(module)s] [%(funcName)s] \
                                %(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='DateFrom, DateTo.')
    parser.add_argument('--df')
    parser.add_argument('--dt')
    parser.add_argument('--mn')
    parser.add_argument('--r')
    parser.add_argument('--tss')
    parser.add_argument('--gs')
    args = parser.parse_args()

    date_from = date_utils.try_parse(args.df)
    date_to = date_utils.try_parse(args.dt)
    model_name = args.mn
    reset_data = args.r == 'true'
    team_stat_season = int(args.tss)
    games_season = int(args.gs)

    AzureModelService(
                model_storage=AzureBlobStorage(
                                        global_config.COMMON['azure_storage_name'],
                                        global_config.COMMON['azure_storage_key'],
                                        model_name),
                data_storage=AzureBlobStorage(
                                        global_config.COMMON['azure_storage_name'],
                                        global_config.COMMON['azure_storage_key'],
                                        '%s-data' % model_name),
                data_source=NHLRefDataSource(team_stat_season=team_stat_season,
                                             games_season=games_season,
                                             cache=DefaultCache.get_instance(),
                                             fvector_len=global_config.MODEL['fvector_length']))\
        .update(date_from=date_from, date_to=date_to, reset_data=reset_data)
