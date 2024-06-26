from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ConfigDict

Base = declarative_base()


class VehicleUpdateOrm(Base):
    __tablename__ = 'vehicle_updates'

    trip_id = Column(String, nullable=False, primary_key=True)
    departure_delay = Column(Integer, nullable=True)
    departure_stop_id = Column(String, nullable=True)
    vehicle = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class VehicleUpdateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trip_id: str
    departure_delay: int | None
    departure_stop_id: str | None
    vehicle: str
    timestamp: datetime
