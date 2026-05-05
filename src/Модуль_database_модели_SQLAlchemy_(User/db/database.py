from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

try:
    from core.config import settings
    DATABASE_URL = settings.DATABASE_URL
except ImportError:
    import os
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todo")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables. Useful for testing only; prefer Alembic migrations."""
    Base.metadata.create_all(bind=engine)
