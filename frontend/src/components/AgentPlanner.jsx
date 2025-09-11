import React, { useState } from 'react';
import { ChevronRight, Sparkles, Calendar, GitBranch, Clock, FileText, Loader2, CheckCircle2, AlertCircle, Zap, Layers, Target, Briefcase, Code, TestTube, Book, Rocket, Copy, Download, Brain, Users, TrendingUp, Award, ArrowRight, Link2, Network } from 'lucide-react';
const AgentPlanner = () => {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showGantt, setShowGantt] = useState(false);
  const [copiedSection, setCopiedSection] = useState('');
  const [animatedTasks, setAnimatedTasks] = useState([]);

  const samplePrompts = [
    "Build a social media dashboard with analytics",
    "Create an e-commerce platform with payment integration",
    "Develop a real-time chat application",
    "Design a task management system with team collaboration"
  ];

  const handleSubmit = async () => {
    if (!description.trim()) {
      setError('Please enter a project description');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      const response = await fetch('https://agentplanner-backend-185237769044.us-central1.run.app/api/v1/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      
      data.tasks?.forEach((task, index) => {
        setTimeout(() => {
          setAnimatedTasks(prev => [...prev, task.id]);
        }, index * 100);
      });
    } catch (err) {
      setError(err.message || 'Failed to generate project plan. Please make sure the backend is running.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      development: <Code className="w-4 h-4" />,
      testing: <TestTube className="w-4 h-4" />,
      documentation: <Book className="w-4 h-4" />,
      deployment: <Rocket className="w-4 h-4" />
    };
    return icons[category] || <Briefcase className="w-4 h-4" />;
  };

  const getCategoryColor = (category) => {
    const colors = {
      development: 'bg-cyan-500',
      testing: 'bg-emerald-500',
      documentation: 'bg-amber-500',
      deployment: 'bg-rose-500'
    };
    return colors[category] || 'bg-indigo-500';
  };

  const getComplexityBadge = (complexity) => {
    const styles = {
      low: 'bg-green-100 text-green-700 border-green-200',
      medium: 'bg-orange-100 text-orange-700 border-orange-200',
      high: 'bg-red-100 text-red-700 border-red-200'
    };
    return styles[complexity] || styles.medium;
  };

  const copyToClipboard = (text, section) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(section);
    setTimeout(() => setCopiedSection(''), 2000);
  };

  const downloadAsJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'project-plan.json';
    a.click();
  };

  const getTaskById = (taskId) => {
    return result?.tasks?.find(t => t.id === taskId);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-cyan-900">
      <style>
        {`
          @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
          @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
          }
          @keyframes pulse-ring {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(1.5); opacity: 0; }
          }
          .floating { animation: float 6s ease-in-out infinite; }
          .pulse-ring { animation: pulse-ring 2s ease-out infinite; }
          .gradient-border {
            background: linear-gradient(45deg, #06b6d4, #3b82f6, #8b5cf6);
            background-size: 200% 200%;
            animation: gradient 3s ease infinite;
          }
        `}
      </style>

      {/* Animated background particles */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -inset-10 opacity-30">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl floating"></div>
          <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl floating" style={{ animationDelay: '2s' }}></div>
          <div className="absolute bottom-1/4 left-1/3 w-96 h-96 bg-teal-500 rounded-full mix-blend-multiply filter blur-3xl floating" style={{ animationDelay: '4s' }}></div>
        </div>
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-white/10 backdrop-blur-lg bg-black/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 pulse-ring bg-cyan-500 rounded-full"></div>
                <Brain className="w-10 h-10 text-cyan-400" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">AgentPlanner</h1>
                <p className="text-cyan-300 text-sm">AI-Powered Project Decomposition</p>
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

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Input Section */}
        <div className="mb-12">
          <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-cyan-400/30 p-8 shadow-2xl">
            <div className="mb-6">
              <label className="block text-white text-lg font-semibold mb-3">
                Describe Your Project
              </label>
              <div className="relative">
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Enter your project idea... (e.g., 'Build a task management app with team collaboration features')"
                  className="w-full px-4 py-3 bg-white/5 border border-cyan-400/30 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-200 resize-none"
                  rows="4"
                />
                <Sparkles className="absolute top-3 right-3 w-5 h-5 text-cyan-400" />
              </div>
            </div>

            <div className="mb-6">
              <p className="text-white/70 text-sm mb-3">Try these examples:</p>
              <div className="flex flex-wrap gap-2">
                {samplePrompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => setDescription(prompt)}
                    className="px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/30 rounded-lg text-cyan-100 text-sm transition-all duration-200 hover:scale-105"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-200 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Generating Project Plan...</span>
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  <span>Generate Project Plan</span>
                  <ChevronRight className="w-5 h-5" />
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl flex items-center space-x-2">
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                <p className="text-red-300 text-sm">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-8">
            {/* Project Overview Card */}
            <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-cyan-400/30 p-8 shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
                  <Target className="w-6 h-6 text-cyan-400" />
                  <span>Project Overview</span>
                </h2>
                <div className="flex space-x-2">
                  <button
                    onClick={() => copyToClipboard(JSON.stringify(result, null, 2), 'overview')}
                    className="p-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg transition-colors"
                  >
                    {copiedSection === 'overview' ? (
                      <CheckCircle2 className="w-5 h-5 text-green-400" />
                    ) : (
                      <Copy className="w-5 h-5 text-white/70" />
                    )}
                  </button>
                  <button
                    onClick={downloadAsJSON}
                    className="p-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg transition-colors"
                  >
                    <Download className="w-5 h-5 text-white/70" />
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gradient-to-br from-cyan-500/20 to-indigo-500/20 rounded-xl p-4 border border-cyan-400/30">
                  <div className="flex items-center space-x-2 mb-2">
                    <Layers className="w-5 h-5 text-cyan-400" />
                    <span className="text-white/70 text-sm">Total Tasks</span>
                  </div>
                  <p className="text-3xl font-bold text-white">{result.tasks?.length || 0}</p>
                </div>
                <div className="bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-xl p-4 border border-emerald-400/30">
                  <div className="flex items-center space-x-2 mb-2">
                    <Clock className="w-5 h-5 text-emerald-400" />
                    <span className="text-white/70 text-sm">Duration</span>
                  </div>
                  <p className="text-3xl font-bold text-white">{result.total_duration || 0} days</p>
                </div>
                <div className="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-xl p-4 border border-indigo-400/30">
                  <div className="flex items-center space-x-2 mb-2">
                    <Calendar className="w-5 h-5 text-indigo-400" />
                    <span className="text-white/70 text-sm">Start Date</span>
                  </div>
                  <p className="text-xl font-bold text-white">
                    {result.start_date ? new Date(result.start_date).toLocaleDateString() : 'Today'}
                  </p>
                </div>
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="flex space-x-2 bg-white/5 p-1 rounded-xl">
              {['overview', 'timeline', 'dependencies', 'export'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all duration-200 ${
                    activeTab === tab
                      ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-lg'
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-cyan-400/30 p-8 shadow-2xl">
              {activeTab === 'overview' && (
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-white mb-4 flex items-center space-x-2">
                    <Layers className="w-5 h-5 text-cyan-400" />
                    <span>Task Breakdown</span>
                  </h3>
                  {result.tasks?.map((task, index) => (
                    <div
                      key={task.id}
                      className={`bg-gradient-to-r from-white/5 to-white/10 rounded-xl p-5 border border-cyan-400/20 transition-all duration-500 transform ${
                        animatedTasks.includes(task.id) ? 'translate-x-0 opacity-100' : '-translate-x-10 opacity-0'
                      } hover:from-white/10 hover:to-white/15 hover:scale-[1.01]`}
                      style={{ transitionDelay: `${index * 50}ms` }}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <div className={`p-2 rounded-lg ${getCategoryColor(task.category)} bg-opacity-20`}>
                            {getCategoryIcon(task.category)}
                          </div>
                          <div className="flex-1">
                            <h4 className="text-white font-semibold text-lg">{task.name}</h4>
                            <p className="text-white/60 text-sm mt-1">{task.description}</p>
                          </div>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getComplexityBadge(task.complexity)}`}>
                          {task.complexity}
                        </span>
                      </div>
                      
                      {/* Dependencies Section - Now Always Visible */}
                      <div className="mt-4 p-3 bg-black/20 rounded-lg">
                        <div className="flex items-center space-x-2 mb-2">
                          <Network className="w-4 h-4 text-cyan-400" />
                          <span className="text-cyan-300 text-sm font-medium">Dependencies</span>
                        </div>
                        {task.dependencies && task.dependencies.length > 0 ? (
                          <div className="flex flex-wrap gap-2">
                            {task.dependencies.map((depId) => {
                              const depTask = getTaskById(depId);
                              return (
                                <div key={depId} className="flex items-center space-x-1 bg-cyan-500/20 px-2 py-1 rounded-lg">
                                  <Link2 className="w-3 h-3 text-cyan-400" />
                                  <span className="text-cyan-100 text-xs">
                                    {depTask?.name || depId}
                                  </span>
                                </div>
                              );
                            })}
                          </div>
                        ) : (
                          <span className="text-white/40 text-xs">No dependencies - Can start immediately</span>
                        )}
                      </div>

                      <div className="flex items-center space-x-4 text-sm text-white/50 mt-3">
                        <span className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{task.duration} days</span>
                        </span>
                        <span className="flex items-center space-x-1">
                          <GitBranch className="w-4 h-4" />
                          <span>{task.dependencies?.length || 0} dependencies</span>
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'timeline' && (
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-white mb-4 flex items-center space-x-2">
                    <Calendar className="w-5 h-5 text-cyan-400" />
                    <span>Project Timeline</span>
                  </h3>
                  <div className="space-y-3">
                    {result.tasks?.map((task, index) => (
                      <div key={task.id} className="flex items-center space-x-4">
                        <div className="w-24 text-white/60 text-sm text-right">
                          Day {Math.floor(task.start_day || index * 3)}
                        </div>
                        <div className="flex-1">
                          <div className="bg-white/5 rounded-lg p-3 border border-cyan-400/20">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-white font-medium">{task.name}</span>
                              <span className="text-white/50 text-sm">{task.duration} days</span>
                            </div>
                            <div className="w-full bg-white/10 rounded-full h-2">
                              <div
                                className="h-2 rounded-full bg-gradient-to-r from-cyan-500 to-indigo-500"
                                style={{ width: `${(task.duration / result.total_duration) * 100}%` }}
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'dependencies' && (
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-white mb-4 flex items-center space-x-2">
                    <Network className="w-5 h-5 text-cyan-400" />
                    <span>Dependency Graph</span>
                  </h3>
                  
                  {/* Visual Dependency Map */}
                  <div className="bg-black/20 rounded-xl p-6 border border-cyan-400/20">
                    <div className="space-y-6">
                      {result.tasks?.map((task) => (
                        <div key={task.id} className="relative">
                          <div className="flex items-start space-x-4">
                            <div className="flex-shrink-0 w-32">
                              <div className="bg-gradient-to-r from-cyan-500/30 to-indigo-500/30 rounded-lg px-3 py-2 border border-cyan-400/30">
                                <p className="text-white font-medium text-sm">{task.name}</p>
                                <p className="text-cyan-300 text-xs mt-1">{task.id}</p>
                              </div>
                            </div>
                            
                            {task.dependencies && task.dependencies.length > 0 ? (
                              <div className="flex-1">
                                <div className="flex items-center space-x-2 mb-2">
                                  <ArrowRight className="w-4 h-4 text-cyan-400" />
                                  <span className="text-white/60 text-sm">Depends on:</span>
                                </div>
                                <div className="grid grid-cols-2 gap-2">
                                  {task.dependencies.map((depId) => {
                                    const depTask = getTaskById(depId);
                                    return (
                                      <div key={depId} className="bg-indigo-500/20 rounded-lg px-3 py-2 border border-indigo-400/30">
                                        <p className="text-white text-sm">{depTask?.name || depId}</p>
                                        <div className="flex items-center space-x-2 mt-1">
                                          <span className={`text-xs px-2 py-0.5 rounded ${getComplexityBadge(depTask?.complexity || 'medium')}`}>
                                            {depTask?.complexity || 'unknown'}
                                          </span>
                                          <span className="text-white/40 text-xs">{depTask?.duration || 0} days</span>
                                        </div>
                                      </div>
                                    );
                                  })}
                                </div>
                              </div>
                            ) : (
                              <div className="flex items-center space-x-2">
                                <CheckCircle2 className="w-4 h-4 text-green-400" />
                                <span className="text-green-300 text-sm">No dependencies - Ready to start</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Dependency Summary */}
                  <div className="grid grid-cols-2 gap-4 mt-6">
                    <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-4 border border-green-400/30">
                      <h4 className="text-white font-medium mb-2">Independent Tasks</h4>
                      <p className="text-green-300 text-sm">
                        {result.tasks?.filter(t => !t.dependencies || t.dependencies.length === 0).length || 0} tasks can start immediately
                      </p>
                    </div>
                    <div className="bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-xl p-4 border border-orange-400/30">
                      <h4 className="text-white font-medium mb-2">Dependent Tasks</h4>
                      <p className="text-orange-300 text-sm">
                        {result.tasks?.filter(t => t.dependencies && t.dependencies.length > 0).length || 0} tasks have prerequisites
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'export' && (
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white mb-4">Export Options</h3>
                  
                  {/* JSON Export */}
                  <div className="space-y-3">
                    <h4 className="text-white font-medium flex items-center space-x-2">
                      <Code className="w-5 h-5 text-cyan-400" />
                      <span>JSON Export</span>
                    </h4>
                    <div className="flex space-x-3">
                      <button
                        onClick={downloadAsJSON}
                        className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-700 hover:to-indigo-700 text-white font-medium rounded-lg transition-all duration-200 flex items-center space-x-2"
                      >
                        <Download className="w-5 h-5" />
                        <span>Download JSON</span>
                      </button>
                      <button
                        onClick={() => copyToClipboard(JSON.stringify(result, null, 2), 'json')}
                        className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/30 text-white font-medium rounded-lg transition-all duration-200 flex items-center space-x-2"
                      >
                        {copiedSection === 'json' ? (
                          <>
                            <CheckCircle2 className="w-5 h-5 text-green-400" />
                            <span>Copied!</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-5 h-5" />
                            <span>Copy JSON</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>

                  {/* Markdown Export */}
                  {result.outputs?.markdown && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <h4 className="text-white font-medium flex items-center space-x-2">
                          <FileText className="w-5 h-5 text-cyan-400" />
                          <span>Markdown Documentation</span>
                        </h4>
                        <button
                          onClick={() => copyToClipboard(result.outputs.markdown, 'markdown')}
                          className="p-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg transition-colors"
                        >
                          {copiedSection === 'markdown' ? (
                            <CheckCircle2 className="w-5 h-5 text-green-400" />
                          ) : (
                            <Copy className="w-5 h-5 text-white/70" />
                          )}
                        </button>
                      </div>
                      <pre className="bg-black/30 rounded-xl p-4 text-cyan-100 text-sm overflow-x-auto">
                        {result.outputs.markdown}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AgentPlanner;