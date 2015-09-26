import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from db import Base

logger = logging.getLogger(__name__)

class UpdateStatModel(Base):
    __tablename__ = 'update_stat_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    status = Column(Integer)
    start_date = Column(DateTime, default=datetime.utcnow())
    end_date = Column(DateTime, nullable=True)

    def __init__(self, name, status=0):
        self.name = name
        # 0 - initial, 1 - in-progress, 2 - finished
        self.status = status
        self.start_date = datetime.utcnow()
