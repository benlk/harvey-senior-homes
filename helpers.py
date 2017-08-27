# Helper functions for the Maine Legislature project
import app_config
import collections
import copytext
import re
import json
import numbers

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
    locations = copy['locations']
    
    for location in locations:
        better_id = location['id'].split('.')

    return locations

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

def get_locations_statuses():
    copy = get_copy()
    statuses = copy['locations_statuses']
    
    for status in statuses:
        if isinstance( status['id'], numbers.Number):
            status['id'] = int(float( status['id'] ))
    return statuses

def get_location_history_by_slug(slug):
    """
    return history, sorted by date then time -> dunno how well this will sort, but we shall see
    """
    locations_statuses = get_locations_statuses()
    history = []

    for row in locations_statuses:
        print row['id']
        print slug
        if row['id'] == slug:
            history.append( row )

        if len( history ) > 1 :
            history = sorted( history, key=itemgetter( 'date', 'time' ), reverse=True )

    return history

def get_location_status_by_slug(slug):
    history = get_location_history_by_slug(slug)
    try:
        return history[0]
    except IndexError:
        return {}

def get_location_status_color_by_slug(slug):
    status = get_location_status_by_slug(slug)
    try:
        if status['color'] not in {'red', 'yellow', 'green', 'grey'}:
            return u'unknown'
        else:
            return status['color']
    except KeyError:
        return u'unknown'

def get_location_status_updated_by_slug(slug):
    status = get_location_status_by_slug(slug)
    try:
        return status['date'] + '' +  status['time']
    except KeyError:
        return u''
