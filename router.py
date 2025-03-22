from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm import Session

from database import Base, engine, new_session
from models import Task
from schrmas import TaskOut, TaskIn

router = APIRouter()

Base.metadata.create_all(bind=engine)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()
        print("Выключение DB")


@router.post("/tasks", response_model=TaskOut)
async def create_task(task_in: TaskIn, db: Session = Depends(get_db)):
    """Пушим таск в БД с проверкой на формат даты"""
    try:
        deadline = datetime.strptime(task_in.deadline, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неправильный формат даты. Пожалуйста, используйте 'ДД-ММ-ГГГГ'.")

    task = Task(title=task_in.title, description=task_in.description, deadline=deadline)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks", response_model=List[TaskOut])
async def get_tasks(db: Session = Depends(get_db)):
    """Получает все наши таски из БД с сортировкой по дате"""
    tasks = db.query(Task).order_by(Task.deadline).all()

    return tasks


@router.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int, db: Session = Depends(get_db)):
    """
    Удаление задачи по её идентификатору.
    id (int): идентификатор задачи.
    Возвращает: None: если задача успешно удалена.
    """
    result = db.execute(delete(Task).where(Task.id == id))
    if not result.rowcount:
        raise HTTPException(status_code=404, detail=f"Задача с ID {id} не найдена.")
    db.commit()
    return None