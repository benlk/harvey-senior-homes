#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
Example application views.

Note that `render_template` is wrapped with `make_response` in all application
routes. While not necessary for most Flask apps, it is required in the
App Template for static publishing.
"""

import app_config
import logging
import oauth
import static

from flask import Flask, make_response, render_template, redirect
from render_utils import make_context, smarty_filter, urlencode_filter
from werkzeug.debug import DebuggedApplication
from helpers import *

app = Flask(__name__)
app.debug = app_config.DEBUG

app.add_template_filter(smarty_filter, name='smarty')
app.add_template_filter(urlencode_filter, name='urlencode')
app.jinja_env.filters['format_zip'] = format_zip
app.jinja_env.filters['status_color'] = get_location_status_color_by_slug
app.jinja_env.filters['status_updated'] = get_location_status_updated_by_slug

logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)

@app.route('/')
@oauth.oauth_required
def index():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    context = make_context()

    return make_response(render_template('index.html', **context))

@app.route('/location')
@app.route('/location/')
@app.route('/locations')
@app.route('/locations/')
def table_redirect():
    """
    redirect people looking for a list of locations to the main page
    """
    return redirect( '/', code='303' ) # 303 See Other

@app.route('/table.html')
def table():
    """
    the pym-child table
    """
    context = make_context()

    return make_response(render_template('table.html', **context))

@app.route('/embedding.html')
def embedding():
    """
    instructions on embedding this item
    """
    context = make_context()

    return make_response(render_template('embedding.html', **context))

@app.route('/embedding.html')
def embedding():
    """
    instructions on embedding this item
    """
    context = make_context()

    return make_response(render_template('embedding.html', **context))

location_ids = get_location_ids()
for slug in location_ids: # 'id' is a __builtin__
    @app.route('/location/%s/' % slug, endpoint=slug)
    def location():
        context = make_context()
        from flask import request

        slug = request.path.split('/')[2]

        context['location'] = get_location_by_slug(slug)
        context['history'] = get_location_history_by_slug(slug)
        context['status'] = get_location_status_by_slug(slug)

        return make_response( render_template( 'location.html', **context ) )

app.register_blueprint(static.static)
app.register_blueprint(oauth.oauth)

# Enable Werkzeug debug pages
if app_config.DEBUG:
    wsgi_app = DebuggedApplication(app, evalex=False)
else:
    wsgi_app = app

# Catch attempts to run the app directly
if __name__ == '__main__':
    logging.error('This command has been removed! Please run "fab app" instead!')
