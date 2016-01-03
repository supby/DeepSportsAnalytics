import os
from flask.ext.assets import Environment, Bundle


def configure_bundle(app):
    bundles = {
        'js_all': Bundle(
            'jquery/dist/jquery.min.js',
            'js/libs/underscore-min.js',
            'js/libs/backbone-min.js',
            'foundation-sites/dist/foundation.min.js',
            'js/libs/foundation-datepicker.min.js',
            'js/libs/moment-with-locales.min.js',
            'js/*.js',
            output='gen/all.js',
            filters='jsmin'),
        'css_all': Bundle(
            'css/libs/*.css',
            'css/*.css',
            Bundle('foundation-sites/assets/foundation.scss', filters='pyscss', depends='**/*.scss'),
            filters='cssmin',
            output='gen/all.css')
    }

    assets = Environment(app)
    assets.load_path = [
        os.path.join(os.path.dirname(__file__), 'static'),
        os.path.join(os.path.dirname(__file__), 'bower_components'),
    ]
    assets.register(bundles)
