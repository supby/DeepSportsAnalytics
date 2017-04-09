import datetime
from dateutil import parser


def try_parse(date_string):
    try:
        return parser.parse(date_string)
    except ex:
        return None
