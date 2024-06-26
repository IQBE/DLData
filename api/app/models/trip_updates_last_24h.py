from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ConfigDict

Base = declarative_base()


class TripUpdatesLast24hORM(Base):
    __tablename__ = 'trip_updates_last_24h'
    __table_args__ = {'schema': 'dbt_schema'}

    amount_of_trip_updates = Column(Integer, nullable=False, primary_key=True)


class TripUpdatesLast24hModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount_of_trip_updates: int
