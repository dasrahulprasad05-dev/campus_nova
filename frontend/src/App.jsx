import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import PlacementPredictor from './components/PlacementPredictor';
import SalaryEstimator from './components/SalaryEstimator';
import ResumeScanner from './components/ResumeScanner';
import AtRiskExplainer from './components/AtRiskExplainer';
import ChatMentor from './components/ChatMentor';
import InterviewVault from './components/InterviewVault';
import AuditHistory from './components/AuditHistory';
import { getHealthStatus } from './services/api';
import { Github, Sparkles } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [backendStatus, setBackendStatus] = useState(null);

  // Shared student candidate profile across modules
  const [profile, setProfile] = useState({
    stream: 'Computer Science',
    cgpa: 7.8,
    internships: 1,
    backlogs: 0,
    student_name: 'Rahul Sharma'
  });

  useEffect(() => {
    async function checkHealth() {
      const res = await getHealthStatus();
      setBackendStatus(res);
    }
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen relative flex flex-col bg-[#030712] text-slate-100 selection:bg-blue-500 selection:text-white">
      
      {/* Dynamic Liquid Mesh Ambient Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        {/* Floating Liquid Orb 1 - Deep Cyan / Electric Blue */}
        <div className="liquid-orb-1 absolute -top-24 -left-20 w-[550px] h-[550px] rounded-full bg-gradient-to-tr from-blue-600/25 via-cyan-500/20 to-indigo-600/10 blur-[120px]" />
        
        {/* Floating Liquid Orb 2 - Purple / Magenta */}
        <div className="liquid-orb-2 absolute top-[30%] -right-28 w-[600px] h-[600px] rounded-full bg-gradient-to-bl from-purple-600/20 via-pink-600/15 to-violet-900/10 blur-[140px]" />
        
        {/* Floating Liquid Orb 3 - Emerald / Ocean Teal */}
        <div className="liquid-orb-3 absolute bottom-[-10%] left-[20%] w-[500px] h-[500px] rounded-full bg-gradient-to-t from-teal-500/15 via-emerald-600/10 to-blue-600/10 blur-[130px]" />
        
        {/* Subtle grid pattern for glass refraction depth */}
        <div 
          className="absolute inset-0 opacity-[0.03] bg-[radial-gradient(#ffffff_1px,transparent_1px)] [background-size:24px_24px]"
        />
      </div>

      {/* Top Floating Liquid Glass Navbar */}
      <div className="relative z-50 pt-3 px-4 sm:px-6 lg:px-8">
        <Navbar 
          activeTab={activeTab} 
          setActiveTab={setActiveTab} 
          backendStatus={backendStatus} 
        />
      </div>

      {/* Main Content Viewport */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'dashboard' && (
          <Dashboard 
            setActiveTab={setActiveTab} 
            backendStatus={backendStatus} 
          />
        )}

        {activeTab === 'predictor' && (
          <PlacementPredictor 
            profile={profile} 
            setProfile={setProfile} 
          />
        )}

        {activeTab === 'salary' && (
          <SalaryEstimator 
            profile={profile} 
            setProfile={setProfile} 
          />
        )}

        {activeTab === 'resume' && (
          <ResumeScanner />
        )}

        {activeTab === 'at-risk' && (
          <AtRiskExplainer 
            profile={profile} 
            setProfile={setProfile} 
          />
        )}

        {activeTab === 'chat' && (
          <ChatMentor />
        )}

        {activeTab === 'interview' && (
          <InterviewVault />
        )}

        {activeTab === 'audit' && (
          <AuditHistory />
        )}
      </main>

      {/* Floating Liquid Glass Footer */}
      <footer className="relative z-10 mt-16 border-t border-white/10 bg-black/40 backdrop-blur-xl py-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-200 tracking-tight">CampusNova AI</span>
            <span className="text-slate-600">•</span>
            <span className="text-slate-400">Liquid Glass Intelligence Platform</span>
          </div>

          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="px-2.5 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">
              FastAPI on Render
            </span>
            <span className="text-slate-600">•</span>
            <a 
              href="https://github.com/dasrahulprasad05-dev/campus_nova"
              target="_blank" 
              rel="noopener noreferrer"
              className="text-slate-300 hover:text-white transition-colors flex items-center gap-1.5"
            >
              <Github className="w-3.5 h-3.5" />
              <span>GitHub</span>
            </a>
          </div>
        </div>
      </footer>

    </div>
  );
}
