from fastapi import APIRouter, Depends
from typing import List

from app.bdconnection import Session
from app.models.vehicle_updates import VehicleUpdateModel, VehicleUpdateOrm
from app.models.avg_delay import AvgDelayModel, AvgDelayORM

router = APIRouter()


def get_db():
    SessionLocal = Session().get_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[VehicleUpdateModel])
async def get_vehicle_updates(ses: Session = Depends(get_db)):
    query = ses.query(VehicleUpdateOrm)
    vu = query.all()
    return vu


@router.get("/trips/{trip_id}", response_model=VehicleUpdateModel)
async def get_vehicle_update(trip_id: str, ses: Session = Depends(get_db)):
    query = ses.query(VehicleUpdateOrm).filter(
        VehicleUpdateOrm.trip_id == trip_id)
    vu = query.first()
    return vu


@router.get("/vehicle/{vehicle}", response_model=List[VehicleUpdateModel])
async def get_vehicle_updates_by_vehicle(vehicle: str, ses: Session = Depends(get_db)):
    query = ses.query(VehicleUpdateOrm).filter(
        VehicleUpdateOrm.vehicle == vehicle)
    vu = query.all()
    return vu


@router.get("/avg_delay", response_model=List[AvgDelayModel])
async def get_avg_delay_per_day(ses: Session = Depends(get_db)):
    query = ses.query(AvgDelayORM)
    vu = query.all()
    return vu
