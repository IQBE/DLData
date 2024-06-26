from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ConfigDict

Base = declarative_base()


class VehiclesMostTripsORM(Base):
    __tablename__ = 'vehicles_most_trips'
    __table_args__ = {'schema': 'dbt_schema'}

    vehicle = Column(Integer, nullable=False, primary_key=True)
    trips = Column(Integer, nullable=False)


class VehiclesMostTripsModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle: int
    trips: int
