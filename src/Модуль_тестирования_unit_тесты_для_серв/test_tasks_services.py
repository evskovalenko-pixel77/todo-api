import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.tasks.services import create_task, get_task, update_task, delete_task
from app.tasks.models import Task

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def sample_task():
    return Task(id=1, title="Test Task", description="desc", completed=False, user_id=1,
                created_at=datetime(2023,1,1), updated_at=datetime(2023,1,1))

def test_create_task(mock_db_session):
    user_id = 1
    title = "New Task"
    description = "A task"
    task = create_task(mock_db_session, user_id, title, description)
    assert task.title == title
    assert task.description == description
    assert task.user_id == user_id
    assert task.completed is False
    mock_db_session.add.assert_called_once_with(task)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(task)

def test_get_task_by_id_owned(mock_db_session, sample_task):
    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_task
    task = get_task(mock_db_session, 1, 1)
    assert task == sample_task

def test_get_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    task = get_task(mock_db_session, 99, 1)
    assert task is None

def test_update_task(mock_db_session, sample_task):
    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_task
    updated = update_task(mock_db_session, 1, 1, {"title": "Updated"})
    assert updated.title == "Updated"
    mock_db_session.commit.assert_called_once()

def test_update_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(ValueError, match="Task not found"):
        update_task(mock_db_session, 1, 1, {"title": "doesn't matter"})

def test_delete_task_success(mock_db_session, sample_task):
    mock_db_session.query.return_value.filter.return_value.first.return_value = sample_task
    delete_task(mock_db_session, 1, 1)
    mock_db_session.delete.assert_called_once_with(sample_task)
    mock_db_session.commit.assert_called_once()

def test_delete_task_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(ValueError, match="Task not found"):
        delete_task(mock_db_session, 1, 1)
