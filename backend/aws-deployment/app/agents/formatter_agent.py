from typing import Dict, Any, List
import json
import csv
from io import StringIO
from datetime import datetime
from app.agents.base_agent import BaseAgent

class FormatterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Formatter")
        
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate multiple output formats for the project plan"""
        
        # No LLM needed for formatting, just process the data
        tasks = state.get('tasks', [])
        dependencies = state.get('dependencies', {})
        
        # Generate all formats
        formats = {
            "gantt_chart": self._generate_gantt_chart(state),
            "json_export": self._generate_json_export(state),
            "csv_export": self._generate_csv_export(state),
            "timeline_visual": self._generate_timeline_visual(state),
            "dependency_graph": self._generate_dependency_graph(state),
            "executive_summary": self._generate_executive_summary(state)
        }
        
        # Update the outputs
        if 'outputs' not in state:
            state['outputs'] = {}
        
        state['outputs'].update(formats)
        
        return state
    
    def _generate_gantt_chart(self, state: Dict[str, Any]) -> str:
        """Generate a Mermaid.js Gantt chart"""
        tasks = state.get('tasks', [])
        
        gantt = "```mermaid\n"
        gantt += "gantt\n"
        gantt += f"    title {state.get('description', 'Project')} - Timeline\n"
        gantt += "    dateFormat YYYY-MM-DD\n"
        gantt += "    axisFormat %m/%d\n\n"
        
        # Group tasks by category
        categories = {}
        for task in tasks:
            cat = task.get('category', 'Other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(task)
        
        # Add sections for each category
        for category, cat_tasks in categories.items():
            gantt += f"    section {category.title()}\n"
            
            for task in cat_tasks:
                task_name = task['name'].replace(':', ' ')[:30]  # Limit length
                task_id = task['id']
                start_date = task.get('start_date', '')
                duration = int(task.get('duration', 1))
                deps = task.get('dependencies', [])
                
                if deps:
                    # Task with dependencies
                    deps_str = ', '.join(deps)
                    gantt += f"    {task_name} ({task_id}) :{task_id}, after {deps[0]}, {duration}d\n"
                else:
                    # Task without dependencies
                    gantt += f"    {task_name} ({task_id}) :{task_id}, {start_date}, {duration}d\n"
        
        gantt += "```\n"
        return gantt
    
    def _generate_json_export(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive JSON export"""
        return {
            "project": {
                "description": state.get('description', ''),
                "created_at": datetime.now().isoformat(),
                "total_duration_days": state.get('total_duration', 0),
                "start_date": state.get('project_start', ''),
                "end_date": state.get('project_end', ''),
            },
            "tasks": state.get('tasks', []),
            "dependencies": state.get('dependencies', {}),
            "execution_plan": {
                "parallel_groups": state.get('parallel_groups', []),
                "critical_path": state.get('critical_path', []),
            },
            "statistics": {
                "total_tasks": len(state.get('tasks', [])),
                "categories": self._count_by_category(state.get('tasks', [])),
                "complexity_distribution": self._count_by_complexity(state.get('tasks', [])),
                "parallelization_factor": len(state.get('parallel_groups', [])),
            }
        }
    
    def _generate_csv_export(self, state: Dict[str, Any]) -> str:
        """Generate CSV export for spreadsheet tools"""
        tasks = state.get('tasks', [])
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = [
            'ID', 'Name', 'Description', 'Category', 'Complexity',
            'Duration (days)', 'Start Date', 'End Date', 'Dependencies'
        ]
        writer.writerow(headers)
        
        # Write task data
        for task in tasks:
            row = [
                task.get('id', ''),
                task.get('name', ''),
                task.get('description', ''),
                task.get('category', ''),
                task.get('complexity', ''),
                task.get('duration', ''),
                task.get('start_date', ''),
                task.get('end_date', ''),
                ', '.join(task.get('dependencies', []))
            ]
            writer.writerow(row)
        
        # Add summary section
        writer.writerow([])  # Empty row
        writer.writerow(['Summary'])
        writer.writerow(['Total Duration (days)', state.get('total_duration', 0)])
        writer.writerow(['Project Start', state.get('project_start', '')])
        writer.writerow(['Project End', state.get('project_end', '')])
        writer.writerow(['Total Tasks', len(tasks)])
        
        return output.getvalue()
    
    def _generate_timeline_visual(self, state: Dict[str, Any]) -> str:
        """Generate ASCII timeline visualization"""
        tasks = state.get('tasks', [])
        if not tasks:
            return "No tasks to visualize"
        
        # Simple ASCII timeline
        timeline = "Project Timeline\n"
        timeline += "=" * 60 + "\n\n"
        
        # Calculate project span
        start_date = datetime.strptime(state.get('project_start', tasks[0]['start_date']), "%Y-%m-%d")
        end_date = datetime.strptime(state.get('project_end', tasks[-1]['end_date']), "%Y-%m-%d")
        total_days = (end_date - start_date).days
        
        # Create timeline header
        timeline += f"Start: {start_date.strftime('%b %d, %Y')}\n"
        timeline += f"End: {end_date.strftime('%b %d, %Y')}\n"
        timeline += f"Duration: {total_days} days\n\n"
        
        # Task timeline
        timeline += "Tasks:\n"
        for task in tasks:
            task_start = datetime.strptime(task['start_date'], "%Y-%m-%d")
            task_end = datetime.strptime(task['end_date'], "%Y-%m-%d")
            
            # Calculate position on timeline
            start_offset = (task_start - start_date).days
            duration = (task_end - task_start).days
            
            # Create visual representation
            timeline += f"{task['id']:8} "
            timeline += " " * start_offset
            timeline += "█" * max(1, duration // 2)  # Scale down for display
            timeline += f" {task['name'][:30]}\n"
        
        return timeline
    
    def _generate_dependency_graph(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate dependency graph data for visualization"""
        tasks = state.get('tasks', [])
        dependencies = state.get('dependencies', {})
        
        # Create nodes
        nodes = []
        for i, task in enumerate(tasks):
            nodes.append({
                "id": task['id'],
                "label": task['name'],
                "category": task['category'],
                "complexity": task['complexity'],
                "duration": task.get('duration', 0),
                "x": (i % 4) * 150,  # Simple grid layout
                "y": (i // 4) * 100
            })
        
        # Create edges
        edges = []
        edge_id = 0
        for task_id, deps in dependencies.items():
            for dep in deps:
                edges.append({
                    "id": f"edge_{edge_id}",
                    "source": dep,
                    "target": task_id,
                    "label": "depends on"
                })
                edge_id += 1
        
        return {
            "nodes": nodes,
            "edges": edges,
            "layout": "hierarchical"
        }
    
    def _generate_executive_summary(self, state: Dict[str, Any]) -> str:
        """Generate executive summary"""
        tasks = state.get('tasks', [])
        total_duration = state.get('total_duration', 0)
        critical_path = state.get('critical_path', [])
        parallel_groups = state.get('parallel_groups', [])
        
        summary = f"""## Executive Summary

**Project Overview**
- Description: {state.get('description', 'N/A')}
- Total Duration: {total_duration} days ({total_duration // 5} weeks)
- Number of Tasks: {len(tasks)}

**Key Metrics**
- Critical Path Length: {len(critical_path)} tasks
- Parallel Execution Phases: {len(parallel_groups)}
- Average Task Duration: {sum(t.get('duration', 0) for t in tasks) / max(len(tasks), 1):.1f} days

**Task Distribution**
"""
        # Add category breakdown
        categories = self._count_by_category(tasks)
        for cat, count in categories.items():
            percentage = (count / len(tasks)) * 100
            summary += f"- {cat.title()}: {count} tasks ({percentage:.0f}%)\n"
        
        summary += "\n**Complexity Analysis**\n"
        complexity = self._count_by_complexity(tasks)
        for comp, count in complexity.items():
            percentage = (count / len(tasks)) * 100
            summary += f"- {comp.title()}: {count} tasks ({percentage:.0f}%)\n"
        
        # Risk factors
        summary += "\n**Risk Factors**\n"
        high_complexity_tasks = [t for t in tasks if t.get('complexity') == 'high']
        if high_complexity_tasks:
            summary += f"- {len(high_complexity_tasks)} high-complexity tasks identified\n"
        
        if len(critical_path) > len(tasks) * 0.7:
            summary += "- Long critical path (limited parallelization)\n"
        
        # Recommendations
        summary += "\n**Recommendations**\n"
        if len(parallel_groups) > 1:
            summary += "- Leverage parallel execution opportunities to reduce timeline\n"
        
        if high_complexity_tasks:
            summary += "- Allocate experienced resources to high-complexity tasks\n"
        
        summary += "- Regular progress monitoring recommended for critical path tasks\n"
        
        return summary
    
    def _count_by_category(self, tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count tasks by category"""
        counts = {}
        for task in tasks:
            cat = task.get('category', 'other')
            counts[cat] = counts.get(cat, 0) + 1
        return counts
    
    def _count_by_complexity(self, tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count tasks by complexity"""
        counts = {}
        for task in tasks:
            comp = task.get('complexity', 'medium')
            counts[comp] = counts.get(comp, 0) + 1
        return counts