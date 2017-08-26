# Helper functions for the Maine Legislature project
import app_config
import collections
import copytext
import re
import json

from unicodedata import normalize

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
