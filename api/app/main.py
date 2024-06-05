from fastapi import FastAPI
from sqlalchemy import text

from app.todos import router as todos_router

app = FastAPI(root_path="/api")

app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the api! Make sure to take a look at the docs at /docs."}