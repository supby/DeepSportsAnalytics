# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "andrej"
__date__ = "$Jun 8, 2015 9:49:09 PM$"

import os
import sys
import logging
import logging.config
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for
from flask import render_template

import global_config
from shared.cache import DefaultCache
from data.source.nhlreference_source import NHLRefDataSource
from api.webapi import webapi
from api.admin import webapi_admin
from db import init_db
from db import db_session

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

def create_app(env):

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    fh = logging.FileHandler('/tmp/deepsportsanalytics.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] [%(process)d:%(thread)d] \
                                    [%(levelname)s] [%(module)s] [%(funcName)s] \
                                    %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    root_logger.addHandler(ch)
    root_logger.addHandler(fh)

    if env == 'dev':
        app.config.from_object('deepsportsanalytics.webapp.config.DevelopmentConfig')
    if env == 'prod':
        app.config.from_object('deepsportsanalytics.webapp.config.ProductionConfig')

    app.logger.addHandler(ch)
    app.logger.addHandler(fh)

    app.register_blueprint(webapi)
    app.register_blueprint(webapi_admin)

    init_db()

    return app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
