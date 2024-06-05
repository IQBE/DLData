from fastapi import APIRouter, Depends
from typing import List

from app.bdconnection import Session
from app.models.todo import TodoModel, TodoOrm, TodoCreate

router = APIRouter()

def get_db():
    SessionLocal = Session().get_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[TodoModel])
async def read_todos(ses: Session = Depends(get_db)):
    query = ses.query(TodoOrm)
    todos = query.filter(TodoOrm.completed == False).all()
    return todos

@router.get("/all", response_model=List[TodoModel])
async def read_todos(ses: Session = Depends(get_db)):
    query = ses.query(TodoOrm)
    todos = query.all()
    return todos

@router.get("/{todo_id}", response_model=TodoModel)
async def read_todo(todo_id: int, ses: Session = Depends(get_db)):
    query = ses.query(TodoOrm)
    todo = query.filter(TodoOrm.todo_id == todo_id).first()
    return todo

@router.put("/complete/{todo_id}", response_model=TodoModel)
async def mark_completed(todo_id: int, ses: Session = Depends(get_db)):
    query = ses.query(TodoOrm)
    todo = query.filter(TodoOrm.todo_id == todo_id).first()
    todo.completed = True
    ses.commit()
    return todo

@router.post("/", response_model=TodoModel)
async def create_todo(todo: TodoCreate, ses: Session = Depends(get_db)):
    new_todo = TodoOrm(**todo.dict())
    ses.add(new_todo)
    ses.commit()
    return new_todo

@router.delete("/{todo_id}", response_model=TodoModel)
async def delete_todo(todo_id: int, ses: Session = Depends(get_db)):
    query = ses.query(TodoOrm)
    todo = query.filter(TodoOrm.todo_id == todo_id).first()
    ses.delete(todo)
    ses.commit()
    return todo