import os
import multiprocessing

import crayons
import maya
from flask import request, current_app, url_for, redirect
from gunicorn import util
from gunicorn.app.base import Application
from whitenoise import WhiteNoise
from flask_cache import Cache

import warnings
from flask.exthook import ExtDeprecationWarning

warnings.simplefilter('ignore', ExtDeprecationWarning)


# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


# \
#  \ji
#  /.(((
#  (,/"(((__,--.
#     \  ) _( /{
#      !|| " :||
#      !||   :||
#       '''   '''

# Gunicorn Stuff
# --------------

def number_of_gunicorn_workers():
    if not 'WEB_CONCURRENCY' in os.environ:
        return (multiprocessing.cpu_count() * 2) + 1
    else:
        return os.environ['WEB_CONCURRENCY']

class WSGIApp(Application):

    def __init__(self, application, options={}):
        """ Construct the Application. Default gUnicorn configuration is loaded """

        self.application = application
        self.usage = None
        self.callable = None
        self.options = options
        self.prog = None
        self.do_load_config()

    def init(self, parser, opts, args):
        """ Apply our custom settings """

        cfg = {}
        for k, v in self.options.items():
            if k.lower() in self.cfg.settings and v is not None:
                cfg[k.lower()] = v
        return cfg

    def load(self):
        """ Attempt an import of the specified application """

        if isinstance(self.application,str):
            return util.import_app(self.application)
        else:
            return self.application

class GunicornServer(object):

    def __init__(self, app, **options):
        """ Construct our application """

        self.app = WSGIApp(app, options)

    def run(self):
        """ Run our application """

        self.app.run()


# Common Stuff
# ------------

class Common(object):
    """Flask-Common."""
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the Flask application with Common."""
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'common' in app.extensions:
            raise RuntimeError("Flask-Common extension already initialized")

        app.extensions['common'] = self
        self.app = app

        if not 'COMMON_FILESERVER_DISABLED' in app.config:
            with app.test_request_context() as c:

                # Configure WhiteNoise.
                app.wsgi_app = WhiteNoise(app.wsgi_app, root=url_for('static', filename='')[1:])

        self.cache = Cache(app, config={'CACHE_TYPE': 'simple'})

        @app.before_request
        def before_request_callback():
            request.start_time = maya.now()

        @app.after_request
        def after_request_callback(response):
            if not 'COMMON_POWERED_BY_DISABLED' in current_app.config:
                response.headers['X-Powered-By'] = 'Flask'
            if not 'COMMON_PROCESSED_TIME_DISABLED' in current_app.config:
                response.headers['X-Processed-Time'] = maya.now().epoch - request.start_time.epoch
            return response

        @app.route('/favicon.ico')
        def favicon():
            return redirect(url_for('static', filename='favicon.ico'), code=301)


    def serve(self, workers=None):
        """Serves the Flask application."""
        if self.app.debug:
            print crayons.yellow('Booting Flask development server...')
            self.app.run()

        else:
            print crayons.yellow('Booting Gunicorn...')

            # Start the web server.
            server = GunicornServer(self.app, workers=workers or number_of_gunicorn_workers())
            server.run()

