from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def _make_db_url() -> str:
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    return "sqlite:///./app.db"


DATABASE_URL = _make_db_url()

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith(
    "sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, future=True,
                       pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True)
