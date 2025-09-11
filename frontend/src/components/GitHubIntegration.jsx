import React from 'react';
import { Github, GitBranch, GitPullRequest, CheckCircle } from 'lucide-react';

const GitHubIntegration = ({ projectData }) => {
  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-cyan-400/30 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-white flex items-center space-x-2">
          <Github className="w-6 h-6 text-cyan-400" />
          <span>GitHub Features</span>
        </h3>
      </div>
      <p className="text-white/70 mb-4">
        Future GitHub integration will include:
      </p>
      <ul className="space-y-2 text-white/60">
        <li className="flex items-center space-x-2">
          <GitBranch className="w-4 h-4 text-cyan-400" />
          <span>Feature branches for each task</span>
        </li>
        <li className="flex items-center space-x-2">
          <GitPullRequest className="w-4 h-4 text-cyan-400" />
          <span>Issues for task tracking</span>
        </li>
        <li className="flex items-center space-x-2">
          <CheckCircle className="w-4 h-4 text-cyan-400" />
          <span>Project board setup</span>
        </li>
      </ul>
    </div>
  );
};

export default GitHubIntegration;