import sys
import datetime
from dateutil import parser
import logging

from flask import Blueprint
from flask import jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from flask import current_app as app

from data.storage.azure_storage import AzureBlobStorage
from shared.cache import DefaultCache
from data.source.nhlreference_source import NHLRefDataSource
from data.source.data_source_factory import DataSourceFactory
from services.data_service import DataService
from services.prediction_service import PredictionService
from utils import date_utils
from statmodel.model_factory import StatModelFactory
from db.repository import StatModelRepository
from db import db_session

logger = logging.getLogger(__name__)

webapi = Blueprint('webapi', __name__)

@webapi.route('/api/v1.0/predict/<modelname>/<datasourcetype>/<datefrom>/<dateto>', methods=['GET'])
def predict(modelname, datasourcetype, datefrom, dateto):
    date_from = date_utils.try_parse(datefrom)
    date_to = date_utils.try_parse(dateto)
    if not date_from:
        logger.error('Error parse date.')
        raise BadRequest
    if not date_to:
        logger.error('Error parse date.')
        raise BadRequest

    try:
        ds = DataService(data_source_factory=DataSourceFactory(app.config))
        X, Y, metadata = \
            ds.get_data(
                data_source_type=datasourcetype,
                filter={"game_date": {"$gte": date_from, "$lt": date_to}})

        if not X:
            return jsonify(data=None)

        ps = PredictionService(
                model_storage=AzureBlobStorage(
                                app.config['AZURE_STORAGE_NAME'],
                                app.config['AZURE_STORAGE_KEY'],
                                'deepsportmodels'))
        predictions = ps.predict(X=X, model_name=modelname)

        return jsonify(data=[{'gameDate': str(pd[1]['game_date']),
                   'team1Name': pd[1]['team1_name'],
                   'team2Name': pd[1]['team2_name'],
                   'winProba': pd[0][1] * 100}
                   for pd in zip(predictions, metadata)])
    except:
        logger.error("%s: Unexpected error: %s" % (__name__, sys.exc_info()))
        raise InternalServerError
