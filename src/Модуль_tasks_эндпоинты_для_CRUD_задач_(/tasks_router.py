from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.auth.dependencies import get_current_user  # returns user_id
from app.db.session import get_db
from . import tasks_schemas, tasks_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[tasks_schemas.TaskResponse])
def list_tasks(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = tasks_service.get_tasks(user_id, db)
    return tasks

@router.post("/", response_model=tasks_schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: tasks_schemas.TaskCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = tasks_service.create_task(task_data, user_id, db)
    return task

@router.get("/{task_id}", response_model=tasks_schemas.TaskResponse)
def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = tasks_service.get_task(task_id, user_id, db)
    return task

@router.patch("/{task_id}", response_model=tasks_schemas.TaskResponse)
def update_task(
    task_id: int,
    task_data: tasks_schemas.TaskUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = tasks_service.update_task(task_id, task_data, user_id, db)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks_service.delete_task(task_id, user_id, db)
    return None  # FastAPI handles 204