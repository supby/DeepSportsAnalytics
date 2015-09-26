import sys
from contextlib import contextmanager
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

engine = create_engine('sqlite:///main.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from db import models
    Base.metadata.create_all(bind=engine)

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
