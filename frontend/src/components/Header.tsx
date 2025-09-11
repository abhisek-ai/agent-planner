import React from 'react';
import { Brain, Users, TrendingUp, Award } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="relative z-10 border-b border-white/10 backdrop-blur-lg bg-black/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="absolute inset-0 animate-pulse-ring bg-purple-500 rounded-full"></div>
              <Brain className="w-10 h-10 text-purple-400" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">AgentPlanner</h1>
              <p className="text-purple-300 text-sm">AI-Powered Project Decomposition</p>
            </div>
          </div>
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-white/70">
              <Users className="w-5 h-5" />
              <span className="text-sm">Multi-Agent System</span>
            </div>
            <div className="flex items-center space-x-2 text-white/70">
              <TrendingUp className="w-5 h-5" />
              <span className="text-sm">30s Generation</span>
            </div>
            <div className="flex items-center space-x-2 text-white/70">
              <Award className="w-5 h-5" />
              <span className="text-sm">Enterprise Ready</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;