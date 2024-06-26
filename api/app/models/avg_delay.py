from datetime import datetime

from sqlalchemy import Column, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ConfigDict

Base = declarative_base()


class AvgDelayORM(Base):
    __tablename__ = 'avg_delay'
    __table_args__ = {'schema': 'dbt_schema'}

    date = Column(DateTime, nullable=False, primary_key=True)
    avg_delay = Column(Float)


class AvgDelayModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: datetime
    avg_delay: float
