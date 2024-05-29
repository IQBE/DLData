from fastapi import APIRouter
from pydantic import BaseModel
from random import randint

router = APIRouter()

class Todo(BaseModel):
    todo_id: int = None
    title: str
    description: str

@router.get("/")
async def read_todos():
    return [
        {"todo_id": 0,"title": "Todo 1", "description": "This is a description of Todo 1"},
        {"todo_id": 1,"title": "Todo 2", "description": "This is a description of Todo 2"}
    ]

@router.get("/{todo_id}")
async def read_todo(todo_id: int):
    return {"todo": f"Todo {todo_id}"}

@router.post("/")
async def create_todo(todo: Todo):
    todo.todo_id = randint(0, 1000)
    return {"new_todo": todo}