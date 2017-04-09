import os
import sys
import logging
import logging.config

from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for
from flask import render_template

from api.webapi import webapi
from db import init_db
from db import db_session
from config import configure_app
from utils import get_instance_folder_path
from bundle_config import configure_bundle

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True)


def create_app(env):
    configure_app(app, env)
    # setup Blueprint
    app.register_blueprint(webapi)
    # init_db()
    configure_bundle(app)

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
