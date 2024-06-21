from fastapi import FastAPI

from app.vehicle_updates.index import router as vehicle_updates_router

app = FastAPI(root_path="/api")

app.include_router(vehicle_updates_router,
                   prefix="/vehicle_updates", tags=["vehicle_updates"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the api! Make sure to take a look at the docs at /docs."}
