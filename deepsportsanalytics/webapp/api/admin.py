import sys
from dateutil import parser
import logging
import threading
import json
from datetime import datetime

from flask import Blueprint
from flask import jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from flask import Response
from sqlalchemy import asc, desc
from flask import current_app as app

from data.storage.azure_storage import AzureBlobStorage
from shared.cache import DefaultCache
from data.source.nhlreference_source import NHLRefDataSource
from utils import date_utils
from utils.thread_utils import AsyncMethod
from db import db_session
from db.repository import StatModelRepository
from db import get_db_session_scope
from services.data_service import DataService
from services.prediction_service import PredictionService
from services.update_service import UpdateService
from data.source.data_source_factory import DataSourceFactory
from statmodel.model_factory import StatModelFactory

logger = logging.getLogger(__name__)

webapi_admin = Blueprint('webapi_admin', __name__)

@AsyncMethod
def __update_async(model_name, date_from, date_to,
                   reset_data, model_status_id, data_source_type):
    logger.info('update_async: model_name=%s, date_from=%s, date_to=%s, \
                reset_data=%s, model_status_id=%s'
                % (model_name, date_from, date_to, reset_data, model_status_id))

    us = UpdateService(
            DataService(data_source_factory=DataSourceFactory(app.config)),
            PredictionService(
                model_storage=AzureBlobStorage(
                                app.config['AZURE_STORAGE_NAME'],
                                app.config['AZURE_STORAGE_KEY'],
                                model_name),
                stat_model_factory=StatModelFactory,
                stat_model_repo=StatModelRepository(db_session)),
            AzureBlobStorage(
                app.config['AZURE_STORAGE_NAME'],
                app.config['AZURE_STORAGE_KEY'],
                '%s-data' % model_name))

    us.update(filter=dict(date_from=date_from, date_to=date_to),
              model_name=model_name,
              data_source_type=data_source_type,
              reset_data=reset_data)

    with get_db_session_scope() as s:
        StatModelRepository(s)\
            .update_history_status(2, model_name, model_status_id)


@webapi_admin.route('/api/v1.0/updatemodel/<modelname>/<datasourcetype>/<datefrom>/<dateto>/<resetdata>', methods=['GET'])
def update_model(modelname, datasourcetype, datefrom, dateto, resetdata):
    """update model throughout web call"""
    date_from = date_utils.try_parse(datefrom)
    date_to = date_utils.try_parse(dateto)
    if not date_from:
        logger.error('[update_model] Error parse date.')
        raise BadRequest
    if not date_to:
        logger.error('[update_model] Error parse date.')
        raise BadRequest

    try:
        rec_id = StatModelRepository(db_session).create_history_rec(modelname)
        __update_async(modelname, date_from, date_to,
                       resetdata=='true', rec_id, datasourcetype)

        return 'Updating started.'
    except:
        db_session.rollback()
        logger.error("%s: Unexpected error: %s" % (__name__, sys.exc_info()))
        raise InternalServerError

@webapi_admin.route('/api/v1.0/updatemodel/status/<modelname>', methods=['GET'])
def get_updating_status(modelname):
    state = StatModelRepository(db_session).get_last_history(modelname)
    return jsonify({ 'id': state.id,
                      'name': state.name,
                      'status': state.status,
                      'start_date': state.start_date,
                      'end_date': state.end_date })


@webapi_admin.route('/api/v1.0/updatemodel/lastupdate/<modelname>', methods=['GET'])
def get_last_update(modelname):
    state = StatModelRepository(db_session).get_last_update(modelname)
    return jsonify({ 'lastUpdate': state.start_date if state else None,
                     'name': modelname })

@webapi_admin.route('/api/v1.0/updatemodel/lastupdate/<modelname>', methods=['GET'])
def set_last_update(modelname):
    pass
