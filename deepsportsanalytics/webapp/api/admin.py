# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "andrej"
__date__ = "$Jun 10, 2015 10:55:52 PM$"

import sys
import datetime
from dateutil import parser
import logging
import threading
import json

from flask import Blueprint
from flask import jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from flask import Response

import global_config
from data.storage.azure_storage import AzureBlobStorage
from shared.cache import DefaultCache
from data.source.source_base import DataSourceFilter
from data.source.nhlreference_source import NHLRefDataSource
from services.model_service_azure import AzureModelService
from utils import date_utils
from utils.thread_utils import AsyncMethod
from db import db_session
from db.models import UpdateStatModel
from extensions.sqlalchemy_ext import AlchemyEncoder
from extensions.sqlalchemy_ext import aljesonify

logger = logging.getLogger(__name__)

webapi_admin = Blueprint('webapi_admin', __name__)

@AsyncMethod
def __update_async(model_name, date_from, date_to, reset_data, done_callback):
    AzureModelService(
                model_storage=AzureBlobStorage(
                                        global_config.COMMON['azure_storage_name'],
                                        global_config.COMMON['azure_storage_key'],
                                        model_name),
                data_storage=AzureBlobStorage(
                                        global_config.COMMON['azure_storage_name'],
                                        global_config.COMMON['azure_storage_key'],
                                        'data'),
                data_source=NHLRefDataSource(dict(sub_data_url=global_config.MINER['sub_data_url'],
                                                  base_url=global_config.MINER['base_url']),
                                             cache=DefaultCache.get_instance(),
                                             fvector_len=global_config.MODEL['fvector_length']))\
        .update(date_from=date_from, date_to=date_to, reset_data=reset_data)
    done_callback()

@webapi_admin.route('/api/v1.0/updatemodel/<modelname>/<datefrom>/<dateto>/<resetdata>', methods=['GET'])
def update_model(modelname, datefrom, dateto, resetdata):
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
        def done_updating():
            UpdateStatModel.query\
                            .filter(UpdateStatModel.name == modelname)\
                            .update({'status': 2})
            db_session.commit()

        __update_async(modelname, date_from, date_to,
                        resetdata=='true', done_updating)

        db_session.add(UpdateStatModel(modelname, 1))
        db_session.commit()

        return 'Updating started.'
    except:
        logger.error("%s: Unexpected error: %s" % (__name__, sys.exc_info()))
        raise InternalServerError

@webapi_admin.route('/api/v1.0/updatemodel/status/<modelname>', methods=['GET'])
def get_updating_status(modelname):
    return aljesonify(UpdateStatModel\
                        .query\
                        .filter(UpdateStatModel.name == modelname)\
                        .first())
