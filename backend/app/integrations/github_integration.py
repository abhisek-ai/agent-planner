from github import Github
from typing import Dict, Any, List, Optional
import os
from fastapi import HTTPException
import base64

class GitHubIntegration:
    def __init__(self, access_token: Optional[str] = None):
        self.token = access_token or os.getenv("GITHUB_TOKEN")
        self.client = Github(self.token) if self.token else None
        
    async def create_project_repository(
        self, 
        project_data: Dict[str, Any],
        org_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new GitHub repository with project structure"""
        
        if not self.client:
            raise HTTPException(status_code=401, detail="GitHub token not configured")
        
        try:
            # Create repository
            user = self.client.get_user()
            repo_name = self._generate_repo_name(project_data['description'])
            
            if org_name:
                org = self.client.get_organization(org_name)
                repo = org.create_repo(
                    name=repo_name,
                    description=project_data['description'],
                    private=False,
                    has_issues=True,
                    has_projects=True,
                    auto_init=True
                )
            else:
                repo = user.create_repo(
                    name=repo_name,
                    description=project_data['description'],
                    private=False,
                    has_issues=True,
                    has_projects=True,
                    auto_init=True
                )
            
            # Create branch structure based on tasks
            await self._create_branch_structure(repo, project_data['tasks'])
            
            # Create initial project structure
            await self._create_project_structure(repo, project_data)
            
            # Create GitHub Issues for tasks
            await self._create_task_issues(repo, project_data['tasks'])
            
            # Create GitHub Project Board
            await self._create_project_board(repo, project_data)
            
            # Setup GitHub Actions
            await self._setup_ci_cd(repo, project_data.get('technology_stack', {}))
            
            return {
                'repository_url': repo.html_url,
                'clone_url': repo.clone_url,
                'branches_created': len(project_data['tasks']),
                'issues_created': len(project_data['tasks']),
                'project_board_url': f"{repo.html_url}/projects/1"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"GitHub integration failed: {str(e)}")
    
    async def _create_branch_structure(self, repo, tasks: List[Dict]):
        """Create feature branches for each task"""
        main_branch = repo.get_branch("main")
        
        for task in tasks:
            branch_name = f"feature/{task['id']}-{self._slugify(task['name'])}"
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=main_branch.commit.sha
            )
    
    async def _create_project_structure(self, repo, project_data: Dict):
        """Create initial folder structure and files"""
        
        # README.md
        readme_content = self._generate_readme(project_data)
        repo.create_file(
            "README.md",
            "Initial commit: Add README",
            readme_content
        )
        
        # Project structure based on tech stack
        tech_stack = project_data.get('technology_stack', {})
        
        if 'frontend' in tech_stack:
            self._create_frontend_structure(repo, tech_stack['frontend'])
        
        if 'backend' in tech_stack:
            self._create_backend_structure(repo, tech_stack['backend'])
        
        # Add .gitignore
        gitignore_content = self._generate_gitignore(tech_stack)
        repo.create_file(
            ".gitignore",
            "Add .gitignore",
            gitignore_content
        )
    
    async def _create_task_issues(self, repo, tasks: List[Dict]):
        """Create GitHub issues for each task"""
        
        for task in tasks:
            labels = [task['category'], f"complexity:{task['complexity']}"]
            
            # Create milestone if it doesn't exist
            milestones = repo.get_milestones()
            milestone = None
            
            issue_body = f"""
## Task Description
{task['description']}

## Details
- **Category**: {task['category']}
- **Complexity**: {task['complexity']}
- **Duration**: {task['duration']} days
- **Dependencies**: {', '.join(task.get('dependencies', []))}

## Acceptance Criteria
{task.get('qa_requirements', {}).get('acceptance_criteria', 'TBD')}

## Resources Needed
{task.get('resources', {}).get('required_roles', 'TBD')}
            """
            
            repo.create_issue(
                title=task['name'],
                body=issue_body,
                labels=labels,
                milestone=milestone
            )
    
    def _generate_readme(self, project_data: Dict) -> str:
        return f"""# {project_data['description']}

## 📋 Project Overview
{project_data['description']}

## 🎯 Project Metrics
- **Total Tasks**: {len(project_data['tasks'])}
- **Duration**: {project_data['total_duration']} days
- **Team Size**: {project_data.get('resource_allocation', {}).get('total_team_size', 'TBD')}
- **Estimated Budget**: ${project_data.get('cost_estimation', {}).get('recommended_budget', 'TBD')}

## 🛠️ Technology Stack
{self._format_tech_stack(project_data.get('technology_stack', {}))}

## 📊 Task Breakdown
{self._format_tasks_table(project_data['tasks'])}

## 🚀 Getting Started
1. Clone the repository
2. Install dependencies
3. Follow setup instructions in /docs

## 👥 Team
{self._format_team(project_data.get('resource_allocation', {}))}

---
*Generated by AgentPlanner AI*
"""