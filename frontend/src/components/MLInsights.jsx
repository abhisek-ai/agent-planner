import React from 'react';
import { Brain, TrendingUp, BarChart3 } from 'lucide-react';

const MLInsights = ({ projectData }) => {
  // Mock predictions based on task count
  const mockPredictions = {
    duration_estimate: projectData.total_duration || 30,
    cost_estimate: (projectData.tasks?.length || 5) * 10000,
    confidence: 0.75
  };

  return (
    <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl border border-purple-400/30 p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Brain className="w-6 h-6 text-purple-400" />
        <h3 className="text-xl font-bold text-white">ML Insights (Demo)</h3>
      </div>
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-black/20 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span className="text-white/70 text-sm">Est. Duration</span>
            </div>
            <p className="text-2xl font-bold text-white">
              {mockPredictions.duration_estimate} days
            </p>
          </div>
          <div className="bg-black/20 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <BarChart3 className="w-4 h-4 text-blue-400" />
              <span className="text-white/70 text-sm">Est. Cost</span>
            </div>
            <p className="text-2xl font-bold text-white">
              ${mockPredictions.cost_estimate.toLocaleString()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MLInsights;