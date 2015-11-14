import os
import sys
import logging
import logging.config
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from data.storage.azure_storage import AzureBlobStorage
from shared.cache import DefaultCache
from data.source.nhlreference_source import NHLRefDataSource
from utils import date_utils
from utils.thread_utils import AsyncMethod
from services.update_service import UpdateService
from services.data_service import DataService
from services.prediction_service import PredictionService
from db.repository import StatModelRepository
from db import get_db_session_scope
from db import init_db

from data.source.data_source_factory import DataSourceFactory
from statmodel.model_factory import StatModelFactory

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
    parser.add_argument('--dst')
    parser.add_argument('--r')
    parser.add_argument('--tss')
    parser.add_argument('--gs')
    args = parser.parse_args()

    date_from = date_utils.try_parse(args.df)
    date_to = date_utils.try_parse(args.dt)
    model_name = args.mn
    data_source_type = args.dst
    reset_data = args.r == 'true'
    team_stat_season = int(args.tss)
    games_season = int(args.gs)

    init_db()

    with get_db_session_scope() as db_session:
        rec_id = StatModelRepository(db_session).create_history_rec(model_name)

        us = UpdateService(DataService(data_source_factory=DataSourceFactory),
                           PredictionService(model_storage=AzureBlobStorage(
                                    global_config.COMMON['azure_storage_name'],
                                    global_config.COMMON['azure_storage_key'],
                                    model_name),
                                    stat_model_factory=StatModelFactory,
                                    stat_model_repo=StatModelRepository(db_session)),
                            AzureBlobStorage(global_config.COMMON['azure_storage_name'],
                                          global_config.COMMON['azure_storage_key'],
                                          '%s-data' % model_name))

        us.update(filter=dict(date_from=date_from, date_to=date_to,
                                    limit=-1, skip_no_score=True),
                  model_name=model_name,
                  data_source_type=data_source_type,
                  reset_data=reset_data)

        # StatModelRepository(db_session)\
        #     .update_history_status(2, model_name, rec_id)
