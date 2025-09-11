from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if os.getenv("K_SERVICE"):
    # Running on Cloud Run
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/agentplanner.db"
else:
    # Local development
    SQLALCHEMY_DATABASE_URL = "sqlite:///./agentplanner.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()