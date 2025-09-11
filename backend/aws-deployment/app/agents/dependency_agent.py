from typing import Dict, Any, List, Set, Tuple
import json
from app.agents.base_agent import BaseAgent

class DependencyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Dependency")
        
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        tasks = state.get('tasks', [])
        
        # Create task summary for the LLM
        task_summary = []
        for task in tasks:
            task_summary.append({
                "id": task["id"],
                "name": task["name"],
                "category": task["category"],
                "description": task["description"]
            })
        
        prompt = f"""
        Analyze these project tasks and identify dependencies between them.
        Tasks: {json.dumps(task_summary, indent=2)}
        
        Rules for dependencies:
        1. Setup/initialization tasks usually have no dependencies
        2. Core development tasks depend on setup tasks
        3. Testing tasks depend on development tasks
        4. Deployment depends on testing
        5. Documentation can often be done in parallel with development
        6. Tasks in the same category might have dependencies if one builds on another
        
        Return a JSON object with:
        {{
            "dependencies": {{
                "task_id": ["list", "of", "dependent", "task_ids"],
                ...
            }},
            "parallel_groups": [
                ["task_ids", "that", "can", "run", "together"],
                ...
            ],
            "critical_path": ["ordered", "list", "of", "task_ids", "forming", "longest", "path"]
        }}
        
        Example:
        {{
            "dependencies": {{
                "task_1": [],
                "task_2": ["task_1"],
                "task_3": ["task_1"],
                "task_4": ["task_2", "task_3"]
            }},
            "parallel_groups": [
                ["task_1"],
                ["task_2", "task_3"],
                ["task_4"]
            ],
            "critical_path": ["task_1", "task_2", "task_4"]
        }}
        
        Return ONLY the JSON object, no other text.
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
            
            dep_data = json.loads(response.strip())
            dependencies = dep_data.get("dependencies", {})
            parallel_groups = dep_data.get("parallel_groups", [])
            critical_path = dep_data.get("critical_path", [])
            
            # Validate dependencies (no cycles)
            if self._has_cycles(dependencies):
                print("Warning: Cycle detected in dependencies, using fallback")
                dependencies = self._create_safe_dependencies(tasks)
                parallel_groups = self._create_parallel_groups(tasks, dependencies)
                critical_path = self._find_critical_path(tasks, dependencies)
            
        except Exception as e:
            print(f"Error in dependency agent: {e}")
            # Fallback to simple sequential dependencies
            dependencies = self._create_safe_dependencies(tasks)
            parallel_groups = self._create_parallel_groups(tasks, dependencies)
            critical_path = self._find_critical_path(tasks, dependencies)
        
        # Update tasks with dependency information
        for task in tasks:
            task_id = task["id"]
            task["dependencies"] = dependencies.get(task_id, [])
        
        # Update timeline based on dependencies
        state = self._adjust_timeline(state, dependencies)
        
        # Add to state
        state["dependencies"] = dependencies
        state["parallel_groups"] = parallel_groups
        state["critical_path"] = critical_path
        
        return state
    
    def _has_cycles(self, dependencies: Dict[str, List[str]]) -> bool:
        """Check if dependency graph has cycles using DFS"""
        visited = set()
        rec_stack = set()
        
        def visit(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for dep in dependencies.get(node, []):
                if visit(dep):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in dependencies:
            if node not in visited:
                if visit(node):
                    return True
        return False
    
    def _create_safe_dependencies(self, tasks: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Create simple, safe dependencies based on task categories"""
        dependencies = {}
        
        # Group tasks by category
        setup_tasks = []
        dev_tasks = []
        test_tasks = []
        deploy_tasks = []
        doc_tasks = []
        
        for task in tasks:
            task_id = task["id"]
            category = task["category"]
            
            if "setup" in task["name"].lower() or "initial" in task["name"].lower():
                setup_tasks.append(task_id)
            elif category == "development":
                dev_tasks.append(task_id)
            elif category == "testing":
                test_tasks.append(task_id)
            elif category == "deployment":
                deploy_tasks.append(task_id)
            elif category == "documentation":
                doc_tasks.append(task_id)
        
        # Create dependencies
        for task in tasks:
            task_id = task["id"]
            deps = []
            
            if task_id in setup_tasks:
                # Setup tasks have no dependencies
                deps = []
            elif task_id in dev_tasks:
                # Dev tasks depend on setup
                deps = setup_tasks[:1]  # Just first setup task
            elif task_id in test_tasks:
                # Test tasks depend on some dev tasks
                deps = dev_tasks[:2] if len(dev_tasks) >= 2 else dev_tasks
            elif task_id in deploy_tasks:
                # Deploy depends on testing
                deps = test_tasks
            elif task_id in doc_tasks:
                # Docs can start after setup
                deps = setup_tasks[:1] if setup_tasks else []
            
            dependencies[task_id] = deps
        
        return dependencies
    
    def _create_parallel_groups(self, tasks: List[Dict[str, Any]], 
                               dependencies: Dict[str, List[str]]) -> List[List[str]]:
        """Group tasks that can be executed in parallel"""
        groups = []
        remaining = set(task["id"] for task in tasks)
        completed = set()
        
        while remaining:
            # Find tasks that can run now
            current_group = []
            for task_id in remaining:
                deps = dependencies.get(task_id, [])
                if all(dep in completed for dep in deps):
                    current_group.append(task_id)
            
            if not current_group:
                # Prevent infinite loop
                current_group = list(remaining)
            
            groups.append(current_group)
            completed.update(current_group)
            remaining.difference_update(current_group)
        
        return groups
    
    def _find_critical_path(self, tasks: List[Dict[str, Any]], 
                           dependencies: Dict[str, List[str]]) -> List[str]:
        """Find the longest path through the dependency graph"""
        # Simple implementation: find path with most dependencies
        task_ids = [t["id"] for t in tasks]
        
        # For each task, find its depth
        depths = {}
        
        def get_depth(task_id):
            if task_id in depths:
                return depths[task_id]
            
            deps = dependencies.get(task_id, [])
            if not deps:
                depths[task_id] = 0
            else:
                depths[task_id] = max(get_depth(dep) for dep in deps) + 1
            
            return depths[task_id]
        
        # Calculate depths
        for task_id in task_ids:
            get_depth(task_id)
        
        # Build critical path
        critical_path = []
        
        # Start with deepest task
        if depths:
            current = max(depths.items(), key=lambda x: x[1])[0]
            
            while current:
                critical_path.insert(0, current)
                deps = dependencies.get(current, [])
                
                if deps:
                    # Choose dependency with highest depth
                    current = max(deps, key=lambda d: depths.get(d, 0))
                else:
                    current = None
        
        return critical_path if critical_path else [task_ids[0]] if task_ids else []
    
    def _adjust_timeline(self, state: Dict[str, Any], 
                        dependencies: Dict[str, List[str]]) -> Dict[str, Any]:
        """Adjust task dates based on dependencies"""
        from datetime import datetime, timedelta
        
        tasks = state.get('tasks', [])
        task_map = {t["id"]: t for t in tasks}
        
        # For each task, ensure it starts after its dependencies end
        for task in tasks:
            task_id = task["id"]
            deps = dependencies.get(task_id, [])
            
            if deps:
                # Find latest end date among dependencies
                latest_end = None
                for dep_id in deps:
                    if dep_id in task_map:
                        dep_task = task_map[dep_id]
                        dep_end = datetime.strptime(dep_task["end_date"], "%Y-%m-%d")
                        if latest_end is None or dep_end > latest_end:
                            latest_end = dep_end
                
                if latest_end:
                    # Adjust this task's start date
                    new_start = latest_end + timedelta(days=1)
                    
                    # Skip weekends
                    while new_start.weekday() >= 5:
                        new_start += timedelta(days=1)
                    
                    # Calculate new end date
                    duration_days = task.get("duration", 5)
                    end_date = new_start
                    days_added = 0
                    
                    while days_added < duration_days:
                        end_date += timedelta(days=1)
                        if end_date.weekday() < 5:
                            days_added += 1
                    
                    task["start_date"] = new_start.strftime("%Y-%m-%d")
                    task["end_date"] = end_date.strftime("%Y-%m-%d")
        
        # Recalculate total project duration
        if tasks:
            all_dates = []
            for task in tasks:
                all_dates.append(datetime.strptime(task["start_date"], "%Y-%m-%d"))
                all_dates.append(datetime.strptime(task["end_date"], "%Y-%m-%d"))
            
            project_start = min(all_dates)
            project_end = max(all_dates)
            total_days = (project_end - project_start).days
            
            state["total_duration"] = total_days
            state["project_start"] = project_start.strftime("%Y-%m-%d")
            state["project_end"] = project_end.strftime("%Y-%m-%d")
        
        return state