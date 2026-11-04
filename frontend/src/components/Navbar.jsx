import React from 'react';
import { 
  GraduationCap, 
  BarChart3, 
  Target, 
  DollarSign, 
  FileText, 
  AlertTriangle, 
  MessageSquareCode, 
  BookOpen, 
  History, 
  ExternalLink,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { API_BASE_URL } from '../services/api';

export default function Navbar({ activeTab, setActiveTab, backendStatus }) {
  const navItems = [
    { id: 'dashboard', label: 'Executive Overview', icon: BarChart3 },
    { id: 'predictor', label: 'Placement Predictor', icon: Target },
    { id: 'salary', label: 'CTC Estimator', icon: DollarSign },
    { id: 'resume', label: 'Resume NLP & Gaps', icon: FileText },
    { id: 'at-risk', label: 'At-Risk (XAI)', icon: AlertTriangle },
    { id: 'chat', label: 'AI Mentor (RAG + Web)', icon: MessageSquareCode },
    { id: 'interview', label: 'Interview Vault', icon: BookOpen },
    { id: 'audit', label: 'Audit Logs', icon: History },
  ];

  const isHealthy = backendStatus?.status === 'ok';

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/85 border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-violet-600 flex items-center justify-center shadow-lg shadow-blue-500/20 ring-1 ring-white/20">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                  CampusNova AI
                </span>
                <span className="text-[10px] font-mono tracking-widest px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30">
                  v1.0 ML
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Predictive Placement & Career Intelligence
              </p>
            </div>
          </div>

          {/* Right Status Pill & GitHub */}
          <div className="flex items-center space-x-3">
            {/* Backend Health Badge */}
            <div 
              className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                isHealthy
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                  : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
              }`}
              title={`Target: ${API_BASE_URL}`}
            >
              <span className="relative flex h-2 w-2">
                {isHealthy && (
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                )}
                <span className={`relative inline-flex rounded-full h-2 w-2 ${isHealthy ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
              </span>
              <span className="font-mono text-[11px]">
                {isHealthy ? 'Render API Live' : 'Connecting API...'}
              </span>
            </div>

            {/* GitHub Link */}
            <a
              href="https://github.com/dasrahulprasad05-dev/campus_nova"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/60 transition-all flex items-center gap-1.5 text-xs font-mono"
              title="View on GitHub"
            >
              <span>GitHub</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

        </div>

        {/* Tab Navigation Navigation Bar */}
        <nav className="flex space-x-1 overflow-x-auto py-2 scrollbar-none border-t border-slate-900/60">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all duration-150 ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/40 shadow-sm shadow-blue-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

      </div>
    </header>
  );
}

