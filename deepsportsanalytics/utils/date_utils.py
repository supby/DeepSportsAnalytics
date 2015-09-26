import datetime
from dateutil import parser

def try_parse(date_string):
    try:
        return datetime.datetime.date(parser.parse(date_string))
    except:
        return None
