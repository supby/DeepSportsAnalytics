import sys
import datetime
from dateutil import parser
import logging

from flask import Blueprint
from flask import jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError

import global_config
from data.storage.azure_storage import AzureBlobStorage
from shared.cache import DefaultCache
from data.source.source_base import DataSourceFilter
from data.source.nhlreference_source import NHLRefDataSource
from services.model_service_azure import AzureModelService
from utils import date_utils

logger = logging.getLogger(__name__)

webapi = Blueprint('webapi', __name__)

@webapi.route('/api/v1.0/predict/<modelname>/<datefrom>/<dateto>', methods=['GET'])
def predict(modelname, datefrom, dateto):
    date_from = date_utils.try_parse(datefrom)
    date_to = date_utils.try_parse(dateto)
    if not date_from:
        logger.error('[predict] Error parse date.')
        raise BadRequest
    if not date_to:
        logger.error('[predict] Error parse date.')
        raise BadRequest

    try:
        data_to_predict, data_to_predict_m, predictions = \
            AzureModelService(
                        model_storage=AzureBlobStorage(
                                                global_config.COMMON['azure_storage_name'],
                                                global_config.COMMON['azure_storage_key'],
                                                modelname),
                        data_storage=AzureBlobStorage(
                                                global_config.COMMON['azure_storage_name'],
                                                global_config.COMMON['azure_storage_key'],
                                                '%s-data' % modelname),
                        data_source=NHLRefDataSource(team_stat_season=2015,
                                                     games_season=2016,
                                                     cache=DefaultCache.get_instance(),
                                                     fvector_len=global_config.MODEL['fvector_length']))\
                    .predict(date_from, date_to)

        if not data_to_predict:
            return jsonify(data=None)

        return jsonify(data=[{'gameDate': str(pd[1][0]),
                   'team1Name': pd[1][1],
                   'team2Name': pd[1][2],
                   'winProba': pd[0][1] * 100}
                   for pd in zip(predictions, data_to_predict_m)])
    except:
        logger.error("%s: Unexpected error: %s" % (__name__, sys.exc_info()))
        raise InternalServerError
