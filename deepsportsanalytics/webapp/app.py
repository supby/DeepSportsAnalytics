# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "andrej"
__date__ = "$Jun 8, 2015 9:49:09 PM$"

import os
import sys
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

import logging
logger = logging.getLogger(__name__)

h = logging.StreamHandler()
h.setLevel(logging.INFO)

l = logging.getLogger()
l.setLevel(logging.INFO)
l.addHandler(h)

app = Flask(__name__)
app.config.from_object('deepsportsanalytics.webapp.config.DevelopmentConfig')
app.logger.addHandler(h)

app.register_blueprint(webapi)
app.register_blueprint(webapi_admin)

init_db()

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predictfile', methods=['GET', 'POST'])
@app.route('/predictfile/', methods=['GET', 'POST'])
def predictfile():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('uploadcsv.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
