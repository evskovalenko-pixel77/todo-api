import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.db.base import Base
from app.db.session import get_db
from app.core.security import create_access_token
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def user_token_headers(db_session, client):
    from app.auth.services import register_user
    email = "testuser@example.com"
    password = "testpassword"
    register_user(db_session, email, password)
    from app.auth.services import authenticate_user
    user = authenticate_user(db_session, email, password)
    token = create_access_token(subject=user.id)
    return {"Authorization": f"Bearer {token}"}
