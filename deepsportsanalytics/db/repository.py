import logging
from datetime import datetime

from sqlalchemy import asc, desc

from db.models import StatModel

logger = logging.getLogger(__name__)

class StatModelRepository(object):
    def __init__(self, db_session):
        self.__db_session = db_session
