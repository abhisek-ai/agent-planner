from typing import Dict, Any
import json
from app.agents.base_agent import BaseAgent

class GitHubAgent(BaseAgent):
    def __init__(self):
        super().__init__("GitHub Agent")
        self.prompt_template = """
You are a GitHub repository architecture expert. Design the optimal repository structure.

Project: {project_description}
Tasks: {tasks}
Tech Stack: {tech_stack}

Provide:
1. repository_structure: Folder hierarchy with key files
2. branch_strategy: Branch naming and workflow (gitflow/github-flow)
3. ci_cd_pipeline: GitHub Actions workflow configuration
4. protection_rules: Branch protection settings
5. team_permissions: Access control recommendations
6. documentation_structure: Where to place different docs
7. commit_conventions: Commit message format
8. pr_template: Pull request template

Return ONLY a JSON object with GitHub configuration.
"""

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Generate GitHub-specific configuration
        prompt = self.prompt_template.format(
            project_description=state.get('project_description'),
            tasks=json.dumps(state.get('tasks', [])),
            tech_stack=json.dumps(state.get('technology_stack', {}))
        )
        
        response = await self.llm.apredict(prompt)
        github_config = json.loads(response.strip())
        state['github_configuration'] = github_config
        
        return state