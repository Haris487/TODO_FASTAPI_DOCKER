from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

## SQLALCHEMY
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import Column, Integer, String 

import schemas

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(Base):
    """
    Defines the todo model
    """

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    def __repr__(self) -> str:
        return f"<Todo {self.title}>"


Base.metadata.create_all(engine)


@app.get("/todos/", response_model=List[schemas.Todo])
def list_todos(db: Session = Depends(get_db)):
    records = db.query(Todo).all()
    return records

@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int,todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return dict(success=True)

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
	db_todo = Todo(title=todo.title, description=todo.description)
	db.add(db_todo)
	db.commit()
	db.refresh(db_todo)
	return db_todo
