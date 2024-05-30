from fastapi import FastAPI
from sqlalchemy import text

from app.todos import router as todos_router
from app.engine import Engine

app = FastAPI(root_path="/api")

app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
async def read_root():
    engine = Engine().get_engine()

    results = []

    with engine.connect() as c:
        res = c.execute(text("SELECT 1 as one"))
        for row in res:
            results.append([x for x in row])

    return {"results": results}