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
  Sparkles
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
    <header className="liquid-glass rounded-2xl px-4 sm:px-6 py-2.5 shadow-2xl transition-all">
      <div className="flex items-center justify-between">
        
        {/* Brand Logo with Liquid Gradient Glow */}
        <div 
          className="flex items-center space-x-3 cursor-pointer group select-none" 
          onClick={() => setActiveTab('dashboard')}
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30 ring-1 ring-white/40 group-hover:scale-105 transition-all">
            <GraduationCap className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg sm:text-xl font-extrabold tracking-tight text-white drop-shadow-sm">
                CampusNova <span className="text-liquid-gradient">AI</span>
              </span>
              <span className="text-[10px] font-mono tracking-widest px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 backdrop-blur-md">
                LIQUID GLASS
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block font-medium">
              B.Tech Placement Predictive Intelligence
            </p>
          </div>
        </div>

        {/* Right Status Pill & GitHub Link */}
        <div className="flex items-center space-x-3">
          {/* Live Microservice Indicator */}
          <div 
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border backdrop-blur-md transition-all ${
              isHealthy
                ? 'bg-emerald-500/15 border-emerald-400/40 text-emerald-300 shadow-sm shadow-emerald-500/20'
                : 'bg-amber-500/15 border-amber-400/40 text-amber-300 shadow-sm shadow-amber-500/20'
            }`}
            title={`Backend URL: ${API_BASE_URL}`}
          >
            <span className="relative flex h-2 w-2">
              {isHealthy && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              )}
              <span className={`relative inline-flex rounded-full h-2 w-2 ${isHealthy ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
            </span>
            <span className="font-mono text-[11px] font-semibold">
              {isHealthy ? 'Render API Live' : 'Connecting API...'}
            </span>
          </div>

          {/* GitHub Pill */}
          <a
            href="https://github.com/dasrahulprasad05-dev/campus_nova"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-mono text-slate-300 hover:text-white bg-white/5 hover:bg-white/10 border border-white/10 transition-all"
            title="View GitHub Repository"
          >
            <span>GitHub</span>
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
        </div>

      </div>

      {/* Liquid Nav Bar Pills */}
      <nav className="flex space-x-1.5 overflow-x-auto pt-3 pb-1 mt-2 border-t border-white/10 scrollbar-none">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 ${
                isActive
                  ? 'bg-gradient-to-r from-blue-600/40 via-indigo-600/40 to-purple-600/40 text-white border border-white/30 shadow-md shadow-blue-500/20 backdrop-blur-md'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-white/5 border border-transparent'
              }`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </header>
  );
}
