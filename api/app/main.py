from fastapi import FastAPI
from todos import router as todos_router

app = FastAPI(root_path="/api")

app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}