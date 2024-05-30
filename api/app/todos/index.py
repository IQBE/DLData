from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.engine import Engine

router = APIRouter()

engine = Engine().get_engine()

class Todo(BaseModel):
    todo_id: int = None
    title: str
    description: str

@router.get("/")
async def read_todos():
    results = []

    with engine.connect() as c:
        res = c.execute(text("SELECT 1 as one"))
        for row in res:
            results.append([x for x in row])

    return results

@router.get("/{todo_id}")
async def read_todo(todo_id: int):
    return 0 # Return the todo

@router.post("/")
async def create_todo(todo: Todo):
    # Add the todo to the database
    return 0 # Return the todo_id