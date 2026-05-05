from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import tasks_models, tasks_schemas


def get_tasks(user_id: int, db: Session) -> list[tasks_models.Task]:
    """Return all tasks for the given user."""
    return db.query(tasks_models.Task).filter(tasks_models.Task.user_id == user_id).all()


def get_task(task_id: int, user_id: int, db: Session) -> tasks_models.Task:
    """Return a specific task if it belongs to the user, otherwise raise 404."""
    task = db.query(tasks_models.Task).filter(
        tasks_models.Task.id == task_id,
        tasks_models.Task.user_id == user_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


def create_task(task_data: tasks_schemas.TaskCreate, user_id: int, db: Session) -> tasks_models.Task:
    """Create a new task for the user."""
    task = tasks_models.Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(task_id: int, task_data: tasks_schemas.TaskUpdate, user_id: int, db: Session) -> tasks_models.Task:
    """Update an existing task. Only allowed fields are changed."""
    task = get_task(task_id, user_id, db)  # raises 404 if not owned
    update_dict = task_data.dict(exclude_unset=True)
    # Validate that at least one field is provided (enforced by schema, but we can double-check)
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No fields to update"
        )
    for key, value in update_dict.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(task_id: int, user_id: int, db: Session) -> None:
    """Delete a task if owned, otherwise raise 404."""
    task = get_task(task_id, user_id, db)
    db.delete(task)
    db.commit()