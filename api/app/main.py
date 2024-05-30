from fastapi import FastAPI
from todos import router as todos_router
import os
from sqlalchemy import create_engine, text

app = FastAPI(root_path="/api")

app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
async def read_root():
    dbhost = os.getenv("DATABASE_HOST", "unknown_host")
    dbuser = os.getenv("DATABASE_USER", "unknown_user")
    dbport = os.getenv("DATABASE_PORT", "unknown_port")
    dbname = os.getenv("DATABASE_NAME", "unknown_name")
    dbpassword = os.getenv("DATABASE_PASSWORD", "unknown_password")

    sqlalchemy_url = f"postgresql+psycopg://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}"

    engine = create_engine(sqlalchemy_url)

    results = []

    with engine.connect() as c:
        res = c.execute(text("SELECT * from pg_stat_activity"))
        for row in res:
            results.append([x for x in row])

    return {"Hello": sqlalchemy_url, "results": results}