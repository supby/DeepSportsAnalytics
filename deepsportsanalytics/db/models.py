import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db import Base

logger = logging.getLogger(__name__)

class StatModel(Base):
    __tablename__ = 'stat_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    model_type = Column(Integer, ForeignKey('stat_model_type.id'), nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow())
    update_date = Column(DateTime, default=datetime.utcnow())

    def __init__(self, name, model_type):
        self.name = name
        self.model_type = model_type
        self.create_date = datetime.utcnow()
        self.update_date = datetime.utcnow()

class StatModelType(Base):
    __tablename__ = 'stat_model_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    create_date = Column(DateTime, default=datetime.utcnow())
    update_date = Column(DateTime, default=datetime.utcnow())

    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.create_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
