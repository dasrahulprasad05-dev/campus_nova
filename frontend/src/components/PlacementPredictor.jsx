import React, { useState } from 'react';
import { 
  Target, 
  Sparkles, 
  CheckCircle, 
  AlertCircle, 
  HelpCircle, 
  ArrowUpRight, 
  RefreshCw,
  Sliders,
  Database
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { predictPlacement } from '../services/api';

const STREAMS = [
  'Computer Science',
  'Information Technology',
  'Electronics And Communication',
  'Mechanical',
  'Electrical',
  'Civil'
];

export default function PlacementPredictor({ profile, setProfile, onPredictComplete }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSliderChange = (field, value) => {
    setProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePredict = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictPlacement(profile);
      setResult(res);
      if (onPredictComplete) onPredictComplete(res);

      if (res.probability >= 80.0) {
        confetti({
          particleCount: 80,
          spread: 60,
          origin: { y: 0.6 }
        });
      }
    } catch (err) {
      setError(err.message || 'Failed to calculate placement probability');
    } finally {
      setLoading(false);
    }
  };

  const prob = result ? result.probability : null;
  const isHighProb = prob !== null && prob >= 50;

  return (
    <div className="py-6 max-w-5xl mx-auto space-y-8">
      
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-mono mb-3">
          <Target className="w-3.5 h-3.5" />
          <span>Feature 1: Placement Likelihood Classification Pipeline</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          B.Tech Placement Probability & What-If Simulator
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Adjust candidate parameters to evaluate offer likelihood based on the 95.26% F1 Decision Tree pipeline.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Form Controls */}
        <div className="lg:col-span-7 glass-panel p-6 sm:p-7 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2 text-white font-semibold text-sm">
              <Sliders className="w-4 h-4 text-blue-400" />
              <span>Candidate Parameters</span>
            </div>
            <span className="text-[11px] font-mono text-slate-400">
              Interactive Sliders
            </span>
          </div>

          {/* Student Name */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 font-mono">
              Student / Candidate Name
            </label>
            <input
              type="text"
              value={profile.student_name || ''}
              onChange={(e) => handleSliderChange('student_name', e.target.value)}
              placeholder="e.g. Rahul Sharma"
              className="input-field"
            />
          </div>

          {/* Stream Selection */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 font-mono">
              Engineering Stream
            </label>
            <select
              value={profile.stream}
              onChange={(e) => handleSliderChange('stream', e.target.value)}
              className="input-field"
            >
              {STREAMS.map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* CGPA Slider */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <label className="font-semibold text-slate-300 font-mono text-xs uppercase">
                Cumulative CGPA
              </label>
              <span className="font-mono font-bold text-lg text-blue-400 bg-blue-500/10 px-2.5 py-0.5 rounded border border-blue-500/20">
                {parseFloat(profile.cgpa).toFixed(1)} / 10.0
              </span>
            </div>
            <input
              type="range"
              min="5.0"
              max="10.0"
              step="0.1"
              value={profile.cgpa}
              onChange={(e) => handleSliderChange('cgpa', parseFloat(e.target.value))}
            />
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>5.0 (Minimum Threshold)</span>
              <span>7.5 (Benchmark)</span>
              <span>10.0 (Perfect)</span>
            </div>
          </div>

          {/* Internships Slider */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <label className="font-semibold text-slate-300 font-mono text-xs uppercase">
                Completed Internships
              </label>
              <span className="font-mono font-bold text-lg text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded border border-indigo-500/20">
                {profile.internships} {profile.internships === 1 ? 'Internship' : 'Internships'}
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="5"
              step="1"
              value={profile.internships}
              onChange={(e) => handleSliderChange('internships', parseInt(e.target.value, 10))}
            />
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>0 (None)</span>
              <span>1 - 2 (Standard)</span>
              <span>5+ (Exemplary)</span>
            </div>
          </div>

          {/* Backlogs Slider */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <label className="font-semibold text-slate-300 font-mono text-xs uppercase">
                History of Active / Past Backlogs
              </label>
              <span className={`font-mono font-bold text-lg px-2.5 py-0.5 rounded border ${
                profile.backlogs === 0 
                  ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' 
                  : 'text-rose-400 bg-rose-500/10 border-rose-500/20'
              }`}>
                {profile.backlogs} {profile.backlogs === 1 ? 'Backlog' : 'Backlogs'}
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="5"
              step="1"
              value={profile.backlogs}
              onChange={(e) => handleSliderChange('backlogs', parseInt(e.target.value, 10))}
            />
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>0 (Clean Record)</span>
              <span>1 - 2 (Borderline)</span>
              <span>5 (High Risk)</span>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={handlePredict}
            disabled={loading}
            className="w-full btn-primary justify-center py-3 text-sm mt-4 font-bold"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running Pipeline Inference...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run Placement Prediction</span>
              </>
            )}
          </button>

          {error && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-5 glass-panel p-6 sm:p-7 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Prediction Diagnostic</span>
            <span className="text-[11px] font-mono text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
              5-Fold Validated
            </span>
          </div>

          {result ? (
            <div className="space-y-6 text-center">
              
              {/* Liquid Radial Score Gauge */}
              <div className="relative inline-flex items-center justify-center p-6">
                <div className={`w-40 h-40 rounded-full border-2 flex flex-col items-center justify-center transition-all ${
                  isHighProb 
                    ? 'border-emerald-400/50 bg-gradient-to-br from-emerald-500/20 via-teal-500/10 to-transparent shadow-[0_0_35px_rgba(16,185,129,0.35),inset_0_2px_4px_rgba(255,255,255,0.4)]' 
                    : 'border-rose-400/50 bg-gradient-to-br from-rose-500/20 via-pink-500/10 to-transparent shadow-[0_0_35px_rgba(244,63,94,0.35),inset_0_2px_4px_rgba(255,255,255,0.4)]'
                }`}>
                  <span className={`text-4xl font-extrabold tracking-tight drop-shadow-md ${
                    isHighProb ? 'text-emerald-300' : 'text-rose-300'
                  }`}>
                    {prob}%
                  </span>
                  <span className="text-[10px] font-mono tracking-widest text-slate-300 uppercase mt-0.5">
                    Likelihood
                  </span>
                </div>
              </div>

              {/* Verdict Banner */}
              <div className={`p-4 rounded-xl border text-sm font-semibold flex items-center justify-center gap-2 ${
                isHighProb
                  ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300'
                  : 'bg-rose-500/15 border-rose-500/40 text-rose-300'
              }`}>
                {isHighProb ? (
                  <CheckCircle className="w-5 h-5 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                )}
                <span>{result.verdict}</span>
              </div>

              {/* Details Metrics */}
              <div className="grid grid-cols-2 gap-3 text-left">
                <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800/80">
                  <div className="text-[10px] font-mono text-slate-400 uppercase">Confidence</div>
                  <div className="text-sm font-bold text-white mt-0.5">{result.confidence}</div>
                </div>
                <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800/80">
                  <div className="text-[10px] font-mono text-slate-400 uppercase">Interaction Term</div>
                  <div className="text-sm font-bold text-blue-400 mt-0.5">
                    {(profile.cgpa * (profile.internships + 1)).toFixed(1)}
                  </div>
                </div>
              </div>

              {/* SQLite Audit confirmation */}
              <div className="text-[11px] font-mono text-slate-400 flex items-center justify-center gap-1.5 pt-2">
                <Database className="w-3.5 h-3.5 text-blue-400" />
                <span>Prediction logged to SQLite (Audit ID: #{result.prediction_id || 'OK'})</span>
              </div>

            </div>
          ) : (
            <div className="py-14 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-slate-500">
                <Target className="w-6 h-6" />
              </div>
              <p className="text-sm text-slate-400">
                Adjust candidate sliders and click <br />
                <span className="text-blue-400 font-semibold">"Run Placement Prediction"</span>
              </p>
            </div>
          )}
        </div>

      </div>

    </div>
  );
}

