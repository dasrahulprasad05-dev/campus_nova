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
import { Heart, Github, Sparkles } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [backendStatus, setBackendStatus] = useState(null);

  // Shared student candidate profile
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
    const interval = setInterval(checkHealth, 30000); // 30s ping
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      
      {/* Top Navbar */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        backendStatus={backendStatus} 
      />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
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

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 backdrop-blur-md py-6 mt-12 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-300">CampusNova AI</span>
            <span>—</span>
            <span>B.Tech Campus Placement Predictive Intelligence</span>
          </div>

          <div className="flex items-center gap-4 text-xs font-mono">
            <span>FastAPI Backend on Render</span>
            <span>•</span>
            <span>React + Vite SPA</span>
            <span>•</span>
            <a 
              href="https://github.com/dasrahulprasad05-dev/campus_nova"
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 flex items-center gap-1"
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

