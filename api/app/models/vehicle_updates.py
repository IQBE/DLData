from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VehicleUpdate(Base):
    __tablename__ = 'vehicle_updates'

    trip_id = Column(String, nullable=False, primary_key=True)
    departure_delay = Column(Integer)
    departure_stop_id = Column(String)
    vehicle = Column(String)
    timestamp = Column(DateTime)
    trip_start_date = Column(DateTime)  # ??? Always null
    trip_schedule_relationship = Column(String)  # ??? Always null
