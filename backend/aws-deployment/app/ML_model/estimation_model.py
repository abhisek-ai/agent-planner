import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from typing import Dict, Any, List, Tuple
import sqlite3
from datetime import datetime

class ProjectEstimationML:
    def __init__(self):
        self.duration_model = None
        self.cost_model = None
        self.complexity_model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.model_path = "models/estimation_models.pkl"
        
    def train_models(self, historical_data: pd.DataFrame):
        """Train ML models on historical project data"""
        
        # Prepare features
        X, y_duration, y_cost = self._prepare_training_data(historical_data)
        
        # Split data
        X_train, X_test, y_dur_train, y_dur_test, y_cost_train, y_cost_test = \
            train_test_split(X, y_duration, y_cost, test_size=0.2, random_state=42)
        
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
        
        # Calculate accuracy metrics
        duration_score = self.duration_model.score(X_test, y_dur_test)
        cost_score = self.cost_model.score(X_test, y_cost_test)
        
        # Save models
        self._save_models()
        
        return {
            'duration_accuracy': duration_score,
            'cost_accuracy': cost_score,
            'training_samples': len(X_train),
            'features_used': X.shape[1]
        }
    
    def predict_task_metrics(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Predict duration and cost for a task using ML"""
        
        if not self.duration_model:
            self._load_models()
        
        # Extract features
        features = self._extract_task_features(task)
        
        # Make predictions
        predicted_duration = self.duration_model.predict([features])[0]
        predicted_cost = self.cost_model.predict([features])[0]
        
        # Calculate confidence intervals
        duration_std = self._calculate_prediction_confidence(
            self.duration_model, [features]
        )
        cost_std = self._calculate_prediction_confidence(
            self.cost_model, [features]
        )
        
        return {
            'predicted_duration': round(predicted_duration, 1),
            'duration_confidence_interval': (
                round(predicted_duration - duration_std, 1),
                round(predicted_duration + duration_std, 1)
            ),
            'predicted_cost': round(predicted_cost, 2),
            'cost_confidence_interval': (
                round(predicted_cost - cost_std, 2),
                round(predicted_cost + cost_std, 2)
            ),
            'confidence_score': self._calculate_confidence_score(task)
        }
    
    def learn_from_completion(self, project_id: str, actual_metrics: Dict):
        """Update models based on actual project completion data"""
        
        # Store actual vs predicted metrics
        self._store_completion_data(project_id, actual_metrics)
        
        # Retrain if enough new data
        if self._should_retrain():
            historical_data = self._load_historical_data()
            self.train_models(historical_data)
    
    def _extract_task_features(self, task: Dict) -> np.array:
        """Extract ML features from task data"""
        
        features = []
        
        # Categorical features
        features.append(self._encode_category(task.get('category', 'development')))
        features.append(self._encode_complexity(task.get('complexity', 'medium')))
        
        # Numerical features
        features.append(len(task.get('dependencies', [])))
        features.append(task.get('team_size', 1))
        features.append(self._calculate_description_complexity(task.get('description', '')))
        
        # Technology stack features
        tech_stack = task.get('tech_stack', {})
        features.append(self._encode_tech_stack(tech_stack))
        
        # Historical performance features
        features.append(self._get_team_performance_score(task.get('team', [])))
        features.append(self._get_similar_project_average(task))
        
        return np.array(features)
    
    def _calculate_description_complexity(self, description: str) -> float:
        """Calculate complexity score from description text"""
        
        # Simple complexity metrics
        word_count = len(description.split())
        technical_terms = self._count_technical_terms(description)
        
        return word_count * 0.1 + technical_terms * 0.5
    
    def _get_similar_project_average(self, task: Dict) -> float:
        """Get average metrics from similar historical tasks"""
        
        # Query historical database for similar tasks
        conn = sqlite3.connect('historical_projects.db')
        cursor = conn.cursor()
        
        query = """
        SELECT AVG(actual_duration) 
        FROM completed_tasks 
        WHERE category = ? AND complexity = ?
        """
        
        result = cursor.execute(
            query, 
            (task.get('category'), task.get('complexity'))
        ).fetchone()
        
        conn.close()
        
        return result[0] if result[0] else 5.0  # Default to 5 days