from celery import Celery
from app.ml.training_pipeline import MLTrainingPipeline
import os

# Create Celery app
celery_app = Celery(
    'agentplanner',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379')
)

@celery_app.task
def train_ml_models():
    """Background task to train ML models"""
    pipeline = MLTrainingPipeline()
    return pipeline.train_models()

@celery_app.task
def collect_project_feedback(project_id: str, actual_metrics: dict):
    """Collect feedback for completed projects"""
    from app.ml.database import SessionLocal, ProjectHistory
    
    session = SessionLocal()
    
    project = session.query(ProjectHistory).filter_by(
        project_id=project_id
    ).first()
    
    if project:
        project.actual_duration = actual_metrics.get('duration')
        project.actual_cost = actual_metrics.get('cost')
        project.completion_rate = actual_metrics.get('completion_rate')
        session.commit()
    
    session.close()
    
    # Trigger retraining if enough new data
    if should_retrain():
        train_ml_models.delay()

def should_retrain() -> bool:
    """Check if we should retrain models"""
    # Implement logic to check if enough new data
    return True  # Placeholder