from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Unicode, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, StringConstraints

Base = declarative_base()

class TodoOrm(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Unicode(255))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
    completed = Column(Boolean, default=False)

class TodoModel(BaseModel):
    todo_id: int
    title: Annotated[str, StringConstraints(max_length=50)]
    description: Annotated[str, StringConstraints(max_length=255)]
    created_at: datetime
    updated_at: datetime
    completed: bool

    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    title: Annotated[str, StringConstraints(max_length=50)]
    description: Annotated[str, StringConstraints(max_length=255)]
    completed: Optional[bool] = False

    class Config:
        orm_mode = True