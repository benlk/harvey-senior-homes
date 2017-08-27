# Helper functions for the Maine Legislature project
import app_config
import collections
import copytext
import re
import json

from unicodedata import normalize
from operator import itemgetter

CACHE = {}

def get_copy():
    """
    Thank you Ryan for this neat trick to avoid thrashing the disk
    https://github.com/INN/maine-legislature/blob/master/helpers.py#L361-L364
    """
    if not CACHE.get('copy', None):
        CACHE['copy'] = copytext.Copy(app_config.COPY_PATH)
    return CACHE['copy']

CACHE = {}

def get_copy():
    """
    Thank you Ryan for this neat trick to avoid thrashing the disk
    https://github.com/INN/maine-legislature/blob/master/helpers.py#L361-L364
    """
    if not CACHE.get('copy', None):
        CACHE['copy'] = copytext.Copy(app_config.COPY_PATH)
    return CACHE['copy']

# Please test the first two lines against "01234-4567": it should not return "001234-4567"
# Please test the first two lines against "61234-4567": it should not return "061234-4567"
def format_zip(zip):
    if type(zip) == str:
        return zip

    try:
        zip = str(zip)
        zip = zip.replace('.0', '')
        return zip
    except ValueError:
        return zip

def get_locations():
    copy = get_copy()
    return copy['locations']

def get_location_ids():
    locations = get_locations()
    ids = []
    for location in locations:
        ids.append(location['id'])
    return ids

def get_location_by_slug(slug):
    locations = get_locations()
    place = None
    for location in locations:
        if location['id'] == slug:
            place = location
            break
        
    return place

def get_location_history_by_slug(slug):
    """
    return history, sorted by date then time -> dunno how well this will sort, but we shall see
    """
    copy = get_copy()
    history = []

    for row in copy['locations_statuses']:
        if row['id'] == slug:
            history.append( row )

        if len( history ) > 1 :
            history = sorted( history, key=itemgetter( 'date', 'time' ), reverse=True )

    return history

def get_location_status_by_slug(slug):
    history = get_location_history_by_slug(slug)
    print history
    status = history[0] if history else []
    if status['color'] not in [u'red', u'yellow', u'green', u'grey']:
        status['color'] = u'unknown'

    return status
