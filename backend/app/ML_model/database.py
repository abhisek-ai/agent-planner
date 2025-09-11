from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ProjectHistory(Base):
    __tablename__ = "project_history"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String, unique=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Predicted vs Actual
    predicted_duration = Column(Float)
    actual_duration = Column(Float)
    predicted_cost = Column(Float)
    actual_cost = Column(Float)
    
    # Features for ML
    task_count = Column(Integer)
    team_size = Column(Integer)
    complexity_score = Column(Float)
    tech_stack = Column(JSON)
    
    # Outcomes
    completion_rate = Column(Float)
    customer_satisfaction = Column(Float)
    
class TaskHistory(Base):
    __tablename__ = "task_history"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    project_id = Column(String)
    
    # Task details
    category = Column(String)
    complexity = Column(String)
    dependencies_count = Column(Integer)
    
    # Predictions vs Actuals
    predicted_duration = Column(Float)
    actual_duration = Column(Float)
    predicted_cost = Column(Float)
    actual_cost = Column(Float)
    
    # Performance metrics
    completion_time = Column(DateTime)
    quality_score = Column(Float)

# Create engine and tables
engine = create_engine('sqlite:///ml_training_data.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)