import pytest
from unittest.mock import MagicMock
from app.auth.services import register_user, authenticate_user
from app.auth.models import User
from app.core.security import hash_password, verify_password

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    # Mock query chain for filter by email
    session.query.return_value.filter.return_value.first.return_value = None
    return session

def test_register_user_success(mock_db_session):
    email = "newuser@example.com"
    password = "securepass"
    user = register_user(mock_db_session, email, password)
    assert user is not None
    assert user.email == email
    assert verify_password(password, user.hashed_password)
    mock_db_session.add.assert_called_once_with(user)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(user)

def test_register_user_email_exists(mock_db_session):
    existing_user = User(email="existing@example.com", hashed_password=hash_password("password"))
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_user
    with pytest.raises(ValueError, match="Email already registered"):
        register_user(mock_db_session, "existing@example.com", "newpass")
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()

def test_authenticate_user_success(mock_db_session):
    email = "user@example.com"
    password = "secret"
    hashed = hash_password(password)
    user = User(email=email, hashed_password=hashed)
    mock_db_session.query.return_value.filter.return_value.first.return_value = user
    result = authenticate_user(mock_db_session, email, password)
    assert result == user

def test_authenticate_user_wrong_password(mock_db_session):
    email = "user@example.com"
    password = "wrong"
    hashed = hash_password("correct")
    user = User(email=email, hashed_password=hashed)
    mock_db_session.query.return_value.filter.return_value.first.return_value = user
    result = authenticate_user(mock_db_session, email, password)
    assert result is None

def test_authenticate_user_user_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    result = authenticate_user(mock_db_session, "noone@example.com", "pass")
    assert result is None
