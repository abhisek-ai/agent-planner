from typing import Dict, Any
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent

class TimelineAgent(BaseAgent):
    def __init__(self):
        super().__init__("Timeline")
        self.duration_map = {
            "low": 2,
            "medium": 5,
            "high": 10
        }
        
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        tasks = state.get('tasks', [])
        current_date = datetime.now()
        total_days = 0
        
        for task in tasks:
            # Get base duration
            complexity = task.get('complexity', 'medium')
            duration = self.duration_map.get(complexity, 5)
            
            # Add buffer (20%)
            duration = duration * 1.2
            
            # Set dates
            task['duration'] = round(duration, 1)
            task['start_date'] = current_date.strftime("%Y-%m-%d")
            
            # Calculate end date (skip weekends)
            end_date = current_date
            days_added = 0
            while days_added < duration:
                end_date += timedelta(days=1)
                if end_date.weekday() < 5:  # Monday-Friday
                    days_added += 1
                    
            task['end_date'] = end_date.strftime("%Y-%m-%d")
            current_date = end_date + timedelta(days=1)
            total_days += duration
            
        state['total_duration'] = int(total_days)
        return state