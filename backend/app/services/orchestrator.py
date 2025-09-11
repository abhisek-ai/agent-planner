from typing import Dict, Any
from app.agents.planner_agent import PlannerAgent
from app.agents.timeline_agent import TimelineAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.formatter_agent import FormatterAgent

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.timeline = TimelineAgent()
        self.dependency = DependencyAgent()
        self.formatter = FormatterAgent()
        
    async def run(self, description: str) -> Dict[str, Any]:
        # Initial state
        state = {
            "description": description,
            "tasks": [],
            "total_duration": 0,
            "dependencies": {},
            "parallel_groups": [],
            "critical_path": []
        }
        
        # Run agents in sequence
        print("Running Planner Agent...")
        state = await self.planner.process(state)
        
        print("Running Timeline Agent...")
        state = await self.timeline.process(state)
        
        print("Running Dependency Agent...")
        state = await self.dependency.process(state)

        print("Running Formatter Agent...") 
        state = await self.formatter.process(state)


        if 'outputs' not in state:
            state['outputs'] = {}
    
        # Ensure we have the basic markdown output
        if 'markdown' not in state['outputs']:
            state['outputs']['markdown'] = self._generate_markdown(state)

        
        # Generate outputs
        state['outputs'] = {
            "markdown": self._generate_markdown(state),
            "summary": {
                "total_tasks": len(state['tasks']),
                "total_duration": state['total_duration'],
                "categories": self._count_categories(state['tasks']),
                "can_parallel": len(state.get('parallel_groups', [])) > 1,
                "critical_path_length": len(state.get('critical_path', [])),
                "dependencies_count": sum(len(deps) for deps in state.get('dependencies', {}).values())
            }
        }

        print(f"Final state keys: {state.keys()}")
        print(f"Tasks count: {len(state.get('tasks', []))}")
        print(f"Outputs keys: {state.get('outputs', {}).keys()}")
        
        return state
    
    def _generate_markdown(self, state: Dict[str, Any]) -> str:
        md = f"# Project Plan\n\n"
        md += f"**Description:** {state['description']}\n"
        md += f"**Total Duration:** {state['total_duration']} days\n"
        md += f"**Project Start:** {state.get('project_start', 'TBD')}\n"
        md += f"**Project End:** {state.get('project_end', 'TBD')}\n\n"
        
        # Add critical path
        critical_path = state.get('critical_path', [])
        if critical_path:
            md += f"**Critical Path:** {' → '.join(critical_path)}\n\n"
        
        # Add parallel execution info
        parallel_groups = state.get('parallel_groups', [])
        if len(parallel_groups) > 1:
            md += "## Parallel Execution Opportunities\n\n"
            for i, group in enumerate(parallel_groups):
                md += f"**Phase {i+1}:** {', '.join(group)}\n"
            md += "\n"
        
        md += "## Tasks\n\n"
        
        for task in state['tasks']:
            md += f"### {task['name']} ({task['id']})\n"
            md += f"- **Description:** {task['description']}\n"
            md += f"- **Category:** {task['category']}\n"
            md += f"- **Duration:** {task['duration']} days\n"
            md += f"- **Dates:** {task['start_date']} to {task['end_date']}\n"
            
            # Add dependencies
            if task.get('dependencies'):
                md += f"- **Depends on:** {', '.join(task['dependencies'])}\n"
            
            md += "\n"
            
        return md
    
    def _count_categories(self, tasks):
        counts = {}
        for task in tasks:
            cat = task.get('category', 'other')
            counts[cat] = counts.get(cat, 0) + 1
        return counts