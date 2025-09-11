import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import schedule
import time
from datetime import datetime
from app.ml.database import SessionLocal, ProjectHistory, TaskHistory

class MLTrainingPipeline:
    def __init__(self):
        self.models_dir = "ml_models/"
        self.duration_model = None
        self.cost_model = None
        self.complexity_model = None
        
    def collect_training_data(self) -> pd.DataFrame:
        """Collect historical project data for training"""
        
        session = SessionLocal()
        
        # Get all completed projects
        projects = session.query(ProjectHistory).filter(
            ProjectHistory.actual_duration.isnot(None)
        ).all()
        
        data = []
        for project in projects:
            # Get associated tasks
            tasks = session.query(TaskHistory).filter_by(
                project_id=project.project_id
            ).all()
            
            # Calculate features
            features = {
                'task_count': project.task_count,
                'team_size': project.team_size,
                'complexity_score': project.complexity_score,
                'avg_task_complexity': np.mean([
                    self._encode_complexity(t.complexity) for t in tasks
                ]),
                'dependency_density': np.mean([
                    t.dependencies_count for t in tasks
                ]) / len(tasks) if tasks else 0,
                'tech_stack_complexity': self._calculate_tech_complexity(
                    project.tech_stack
                ),
                'actual_duration': project.actual_duration,
                'actual_cost': project.actual_cost
            }
            data.append(features)
        
        session.close()
        return pd.DataFrame(data)
    
    def train_models(self):
        """Train ML models with latest data"""
        
        print(f"[{datetime.now()}] Starting ML training pipeline...")
        
        # Collect data
        df = self.collect_training_data()
        
        if len(df) < 10:
            print("Not enough data for training (need at least 10 projects)")
            return
        
        # Prepare features and targets
        feature_cols = [
            'task_count', 'team_size', 'complexity_score',
            'avg_task_complexity', 'dependency_density', 'tech_stack_complexity'
        ]
        
        X = df[feature_cols]
        y_duration = df['actual_duration']
        y_cost = df['actual_cost']
        
        # Split data
        X_train, X_test, y_dur_train, y_dur_test = train_test_split(
            X, y_duration, test_size=0.2, random_state=42
        )
        
        _, _, y_cost_train, y_cost_test = train_test_split(
            X, y_cost, test_size=0.2, random_state=42
        )
        
        # Train duration model
        self.duration_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.duration_model.fit(X_train, y_dur_train)
        
        # Train cost model
        self.cost_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.cost_model.fit(X_train, y_cost_train)
        
        # Evaluate models
        dur_pred = self.duration_model.predict(X_test)
        cost_pred = self.cost_model.predict(X_test)
        
        metrics = {
            'duration_mae': mean_absolute_error(y_dur_test, dur_pred),
            'duration_r2': r2_score(y_dur_test, dur_pred),
            'cost_mae': mean_absolute_error(y_cost_test, cost_pred),
            'cost_r2': r2_score(y_cost_test, cost_pred),
            'training_samples': len(X_train),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"Training completed! Metrics: {metrics}")
        
        # Save models
        self.save_models()
        
        return metrics
    
    def save_models(self):
        """Save trained models to disk"""
        
        import os
        os.makedirs(self.models_dir, exist_ok=True)
        
        if self.duration_model:
            joblib.dump(
                self.duration_model,
                f"{self.models_dir}duration_model.pkl"
            )
        
        if self.cost_model:
            joblib.dump(
                self.cost_model,
                f"{self.models_dir}cost_model.pkl"
            )
        
        print(f"Models saved to {self.models_dir}")
    
    def load_models(self):
        """Load pre-trained models"""
        
        import os
        
        duration_path = f"{self.models_dir}duration_model.pkl"
        cost_path = f"{self.models_dir}cost_model.pkl"
        
        if os.path.exists(duration_path):
            self.duration_model = joblib.load(duration_path)
        
        if os.path.exists(cost_path):
            self.cost_model = joblib.load(cost_path)
    
    def predict(self, features: dict) -> dict:
        """Make predictions for new project"""
        
        if not self.duration_model or not self.cost_model:
            self.load_models()
        
        if not self.duration_model:
            return {
                'error': 'No trained models available',
                'duration_estimate': 30,
                'cost_estimate': 50000
            }
        
        # Prepare feature vector
        feature_vector = [
            features.get('task_count', 5),
            features.get('team_size', 3),
            features.get('complexity_score', 5),
            features.get('avg_task_complexity', 2),
            features.get('dependency_density', 0.3),
            features.get('tech_stack_complexity', 5)
        ]
        
        # Make predictions
        duration_pred = self.duration_model.predict([feature_vector])[0]
        cost_pred = self.cost_model.predict([feature_vector])[0]
        
        return {
            'duration_estimate': round(duration_pred, 1),
            'cost_estimate': round(cost_pred, 2),
            'confidence': self._calculate_confidence(features),
            'model_version': 'v1.0'
        }
    
    def _encode_complexity(self, complexity: str) -> int:
        mapping = {'low': 1, 'medium': 2, 'high': 3}
        return mapping.get(complexity, 2)
    
    def _calculate_tech_complexity(self, tech_stack: dict) -> float:
        if not tech_stack:
            return 5.0
        
        # Simple heuristic based on number of technologies
        return min(len(tech_stack) * 1.5, 10)
    
    def _calculate_confidence(self, features: dict) -> float:
        # Simple confidence based on data availability
        confidence = 0.5
        
        if features.get('task_count'):
            confidence += 0.1
        if features.get('team_size'):
            confidence += 0.1
        if features.get('complexity_score'):
            confidence += 0.1
        if features.get('tech_stack_complexity'):
            confidence += 0.1
        if self.duration_model and self.cost_model:
            confidence += 0.1
        
        return min(confidence, 0.95)

# Schedule training pipeline
def run_scheduled_training():
    pipeline = MLTrainingPipeline()
    
    # Train immediately on startup
    pipeline.train_models()
    
    # Schedule weekly retraining
    schedule.every().sunday.at("02:00").do(pipeline.train_models)
    
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour