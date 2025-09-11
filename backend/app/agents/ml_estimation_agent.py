from typing import Dict, Any
import json
from app.agents.base_agent import BaseAgent
from app.ml.estimation_model import ProjectEstimationML

class MLEstimationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ML Estimation Agent")
        self.ml_model = ProjectEstimationML()
        
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance estimates using ML predictions"""
        
        tasks = state.get('tasks', [])
        ml_enhanced_tasks = []
        
        for task in tasks:
            # Get ML predictions
            ml_predictions = self.ml_model.predict_task_metrics(task)
            
            # Combine with agent estimates
            task['ml_duration'] = ml_predictions['predicted_duration']
            task['ml_cost'] = ml_predictions['predicted_cost']
            task['confidence_score'] = ml_predictions['confidence_score']
            
            # Adjust original estimates based on ML confidence
            if ml_predictions['confidence_score'] > 0.8:
                # High confidence - weight ML predictions more
                task['adjusted_duration'] = (
                    task['duration'] * 0.3 + 
                    ml_predictions['predicted_duration'] * 0.7
                )
            else:
                # Low confidence - weight original estimates more
                task['adjusted_duration'] = (
                    task['duration'] * 0.7 + 
                    ml_predictions['predicted_duration'] * 0.3
                )
            
            ml_enhanced_tasks.append(task)
        
        state['tasks'] = ml_enhanced_tasks
        state['ml_analysis'] = {
            'models_used': True,
            'average_confidence': sum(t['confidence_score'] for t in tasks) / len(tasks),
            'training_data_size': self.ml_model.get_training_size()
        }
        
        return state