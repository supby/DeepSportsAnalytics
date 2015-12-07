import logging
from datetime import datetime

from sqlalchemy import asc, desc

from db.models import StatModel
from db.models import UpdateStatModelHistory

logger = logging.getLogger(__name__)

class StatModelRepository(object):
    def __init__(self, db_session):
        self.__db_session = db_session

    def create_history_rec(self, model_name):
        logger.info('create history record: model_name = %s' % model_name)

        rec = UpdateStatModelHistory(model_name, 1)
        self.__db_session.add(rec)
        self.__db_session.commit()

        return rec.id

    def update_history_status(self, status, model_name, rec_id):
        UpdateStatModelHistory.query\
                        .filter(UpdateStatModelHistory.name == model_name,\
                                UpdateStatModelHistory.id == rec_id)\
                        .update({'status': status, 'end_date': datetime.utcnow() })
        self.__db_session

    def get_last_history(self, model_name):
        return UpdateStatModelHistory\
                            .query\
                            .filter(UpdateStatModelHistory.name == model_name)\
                            .order_by(desc(UpdateStatModelHistory.id))\
                            .first()

    def get_last_update(self, model_name):
        state = UpdateStatModelHistory\
                            .query\
                            .filter(UpdateStatModelHistory.name == model_name,
                                    UpdateStatModelHistory.status == 2)\
                            .order_by(desc(UpdateStatModelHistory.id))\
                            .first()
