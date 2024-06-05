from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from datetime import datetime

from app.bdconnection import Session

router = APIRouter()

SessionLocal = Session().get_session()

class Todo(BaseModel):
    todo_id: int = None
    title: str
    description: str
    created_at: datetime = None
    updated_at: datetime = None
    completed: bool = False

@router.get("/")
async def read_todos():
    results = []

    with SessionLocal() as ses:
        res = ses.execute(text("SELECT * FROM todos WHERE completed = false"))
        for row in res:
            results.append([x for x in row])

    return results

@router.get("/all")
async def read_todos():
    results = []

    with SessionLocal() as ses:
        res = ses.execute(text("SELECT * from todos"))
        for row in res:
            results.append([x for x in row])

    return results

@router.get("/{todo_id}")
async def read_todo(todo_id: int):
    results = []

    with SessionLocal() as ses:
        res = ses.execute(text(f"SELECT * from todos WHERE todo_id = {todo_id}"))
        for row in res:
            results.append([x for x in row])

    return results

@router.put("/complete/{todo_id}")
async def mark_completed(todo_id: int):
    with SessionLocal() as ses:
        res = ses.execute(text(f"UPDATE todos SET completed = true WHERE todo_id = {todo_id} RETURNING *"))
        row = res.fetchone()

        if not row:
            return "Failed to mark todo as completed"

        todoResp = Todo(
            todo_id=row[0],
            title=row[1],
            description=row[2],
            created_at=row[3],
            updated_at=row[4],
            completed=row[5]
        )

        ses.commit()
    return todoResp

@router.post("/")
async def create_todo(todo: Todo):
    with SessionLocal() as ses:
        res = ses.execute(text(f"INSERT INTO todos (title, description) VALUES ('{todo.title}', '{todo.description}') RETURNING *"))
        row = res.fetchone()

        if not row:
            return "Failed to create todo"

        todoResp = Todo(
            todo_id=row[0],
            title=row[1],
            description=row[2],
            created_at=row[3],
            updated_at=row[4],
            completed=row[5]
        )

        ses.commit()
    return todoResp

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    with SessionLocal() as ses:
        res = ses.execute(text(f"DELETE FROM todos WHERE todo_id = {todo_id} RETURNING *"))
        row = res.fetchone()

        if not row:
            return "Failed to delete todo"

        todoResp = Todo(
            todo_id=row[0],
            title=row[1],
            description=row[2],
            created_at=row[3],
            updated_at=row[4],
            completed=row[5]
        )

        ses.commit()
    return todoResp