import sys
from contextlib import contextmanager
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///deepsport.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
    populate()

@contextmanager
def get_db_session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db_session()
    try:
        yield session
    except exc.SQLAlchemyError, e:
        logger.error('DB Session error -> %s' % e)
        session.rollback()
        raise
    except:
        session.rollback()
        logger.error('DB Session -> unexpected error: %s, %s' %
                  (sys.exc_info()[0], sys.exc_info()[1]))
        raise
    finally:
        session.close()

def populate():
    from db.models import *
    session = db_session()
    # fill models types
    if session.query(StatModelType).filter(StatModelType.name=='scikitmodel').count() == 0:
        session.add(StatModelType('scikitmodel'))
        session.commit()
    if session.query(StatModelType).filter(StatModelType.name=='dnnmodel').count() == 0:
        session.add(StatModelType('dnn'))
        session.commit()
    # fill stat models
    scmodel_type = session.query(StatModelType).filter(StatModelType.name=='scikitmodel').first()
    dnn_type = session.query(StatModelType).filter(StatModelType.name=='dnn').first()
    if session.query(StatModel).filter(StatModel.name=='model',
                                       StatModel.type==scmodel_type.id).count() == 0:
        session.add(StatModel('model', scmodel_type.id))
        session.commit()
    if session.query(StatModel).filter(StatModel.name=='dnn_model',
                                       StatModel.type==dnn_type.id).count() == 0:
        session.add(StatModel('model', dnn_type.id))
        session.commit()
