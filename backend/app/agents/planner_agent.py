from typing import Dict, Any, List
import json
from app.agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Planner")
        
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Break down this project into 5-8 specific tasks:
        "{state['description']}"
        
        Return a JSON array with tasks, each having:
        - id: (task_1, task_2, etc.)
        - name: (short descriptive name)
        - description: (1-2 sentences)
        - category: (development/testing/documentation/deployment)
        - complexity: (low/medium/high)
        
        Example:
        [{{"id": "task_1", "name": "Setup Environment", "description": "Initialize project", "category": "development", "complexity": "low"}}]
        
        Return ONLY the JSON array, no other text.
        """
        
        try:
            message = await self.llm.ainvoke(prompt)
            response = message.content
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            tasks = json.loads(response.strip())
            state['tasks'] = tasks[:8]  # Limit to 8 tasks
            
        except Exception as e:
            print(f"Error in planner: {e}")
            # Fallback tasks
            state['tasks'] = [
                {
                    "id": "task_1",
                    "name": "Project Setup",
                    "description": "Initialize project structure",
                    "category": "development",
                    "complexity": "medium"
                },
                {
                    "id": "task_2", 
                    "name": "Core Development",
                    "description": "Build main features",
                    "category": "development",
                    "complexity": "medium"
                },
                {
                    "id": "task_3",
                    "name": "Testing",
                    "description": "Test the application",
                    "category": "testing",
                    "complexity": "medium"
                }
            ]
        
        return state