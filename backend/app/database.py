"""
Database configuration for OIL SIF-Sentinel.
Defaults to SQLite file database for immediate zero-config execution,
and automatically connects to PostgreSQL if DATABASE_URL is defined.
"""

import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

VERCEL_ENV = os.getenv("VERCEL")
DB_PATH = "./oil_safety.db"

if VERCEL_ENV:
    # On Vercel, the filesystem is read-only except for /tmp.
    # We must copy the bundled SQLite DB to /tmp to allow writes!
    tmp_db_path = "/tmp/oil_safety.db"
    if not os.path.exists(tmp_db_path):
        possible_paths = ["./oil_safety.db", "backend/oil_safety.db", "../backend/oil_safety.db", "../../backend/oil_safety.db", "oil_safety.db"]
        for p in possible_paths:
            if os.path.exists(p):
                shutil.copy2(p, tmp_db_path)
                break
    DB_PATH = tmp_db_path

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# SQLite requires check_same_thread=False for multi-threaded FastAPI handlers
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
