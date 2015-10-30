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
from data.source.data_source_factory import DataSourceFactory
from services.model_service_azure import AzureModelService
from services.data_service import DataService
from services.prediction_service import PredictionService
from utils import date_utils
from statmodel.model_factory import StatModelFactory
from db.repository import StatModelRepository
from db import db_session

logger = logging.getLogger(__name__)

webapi = Blueprint('webapi', __name__)

@webapi.route('/api/v1.0/predict/<modelname>/<datefrom>/<dateto>', methods=['GET'])
def predict(modelname, data_source_type, datefrom, dateto):
    date_from = date_utils.try_parse(datefrom)
    date_to = date_utils.try_parse(dateto)
    if not date_from:
        logger.error('[predict] Error parse date.')
        raise BadRequest
    if not date_to:
        logger.error('[predict] Error parse date.')
        raise BadRequest

    try:
        ds = DataService(data_storage=AzureBlobStorage(
                                global_config.COMMON['azure_storage_name'],
                                global_config.COMMON['azure_storage_key'],
                                '%s-data' % modelname),
                    data_source_factory=DataSourceFactory())
        data_to_predict, data_to_predict_m = \
            ds.get_data(data_source_type='hnlref',
                        filter=DataSourceFilter(date_from=date_from,
                                                date_to=date_to,
                                                limit=-1))

        ps = PredictionService(model_storage=AzureBlobStorage(
                                global_config.COMMON['azure_storage_name'],
                                global_config.COMMON['azure_storage_key'],
                                modelname),
            stat_model_factory=StatModelFactory,
            stat_model_repo=StatModelRepository(db_session))
        predictions = ps.predict(data=data_to_predict[0],
                                model_name=modelname)

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
