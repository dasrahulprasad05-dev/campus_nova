import React, { useState } from 'react';
import { 
  DollarSign, 
  TrendingUp, 
  Award, 
  Sparkles, 
  RefreshCw, 
  AlertCircle,
  Briefcase,
  Zap
} from 'lucide-react';
import { predictSalary } from '../services/api';

export default function SalaryEstimator({ profile, setProfile }) {
  const [aptitudeScore, setAptitudeScore] = useState(78);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleEstimate = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await predictSalary({
        cgpa: profile.cgpa,
        internships: profile.internships,
        aptitude_score: aptitudeScore
      });
      setResult(res);
    } catch (err) {
      setError(err.message || 'Failed to estimate expected CTC');
    } finally {
      setLoading(false);
    }
  };

  const getTier = (lpa) => {
    if (lpa >= 10.0) return { name: 'Super Dream / High Growth MNC', color: 'text-purple-400 bg-purple-500/10 border-purple-500/30' };
    if (lpa >= 6.5) return { name: 'Product Engineering Tier', color: 'text-blue-400 bg-blue-500/10 border-blue-500/30' };
    if (lpa >= 4.5) return { name: 'Core Technology Tier', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' };
    return { name: 'Entry Enterprise / Mass Recruiter', color: 'text-amber-400 bg-amber-500/10 border-amber-500/30' };
  };

  return (
    <div className="py-6 max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono mb-3">
          <DollarSign className="w-3.5 h-3.5" />
          <span>Feature 2: Expected CTC Salary Package Regressor</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          Expected CTC Salary Estimator
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Predict compensation packages (LPA) driven by Ridge Regression trained on verified Kaggle salary profiles (±0.21 LPA MAE).
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Controls */}
        <div className="lg:col-span-7 glass-panel p-6 sm:p-7 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Evaluation Factors</span>
            <span className="text-[11px] font-mono text-slate-400">Ridge Regressor</span>
          </div>

          {/* Academic CGPA */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <label className="font-semibold text-slate-300 font-mono text-xs uppercase">
                Undergraduate CGPA
              </label>
              <span className="font-mono font-bold text-base text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                {parseFloat(profile.cgpa).toFixed(1)} / 10.0 (≈ {(profile.cgpa * 9.5).toFixed(1)}%)
              </span>
            </div>
            <input
              type="range"
              min="5.0"
              max="10.0"
              step="0.1"
              value={profile.cgpa}
              onChange={(e) => setProfile(prev => ({ ...prev, cgpa: parseFloat(e.target.value) }))}
            />
          </div>

          {/* Employability Aptitude Score */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <label className="font-semibold text-slate-300 font-mono text-xs uppercase">
                Campus Aptitude & E-Test Score
              </label>
              <span className="font-mono font-bold text-base text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
                {aptitudeScore}%
              </span>
            </div>
            <input
              type="range"
              min="40"
              max="100"
              step="1"
              value={aptitudeScore}
              onChange={(e) => setAptitudeScore(parseInt(e.target.value, 10))}
            />
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>40% (Passing)</span>
              <span>75% (Competitive)</span>
              <span>100% (Top Decile)</span>
            </div>
          </div>

          {/* Internship Status */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between">
            <div>
              <div className="text-sm font-semibold text-white">Prior Industry Internship</div>
              <div className="text-xs text-slate-400 mt-0.5">
                {profile.internships > 0 ? `${profile.internships} completed internship(s)` : 'No internships recorded'}
              </div>
            </div>
            <button
              onClick={() => setProfile(prev => ({ ...prev, internships: prev.internships > 0 ? 0 : 1 }))}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                profile.internships > 0
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-slate-800 text-slate-400 border border-slate-700'
              }`}
            >
              {profile.internships > 0 ? 'Experience Active' : 'No Experience'}
            </button>
          </div>

          {/* Button */}
          <button
            onClick={handleEstimate}
            disabled={loading}
            className="w-full btn-primary justify-center py-3 text-sm mt-4 font-bold"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Computing Package Projections...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Estimate Expected CTC</span>
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

        {/* Results */}
        <div className="lg:col-span-5 glass-panel p-6 sm:p-7 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Package Projection</span>
            <span className="text-[11px] font-mono text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
              ±0.21 LPA MAE
            </span>
          </div>

          {result ? (
            <div className="space-y-6">
              {/* Liquid Main CTC Display */}
              <div className="text-center py-6 bg-gradient-to-br from-indigo-600/20 via-purple-600/15 to-blue-600/10 rounded-2xl border border-white/20 shadow-[inset_0_2px_4px_rgba(255,255,255,0.25),0_15px_35px_rgba(99,102,241,0.25)] backdrop-blur-xl p-6">
                <span className="text-xs font-mono tracking-widest text-indigo-300 uppercase">
                  Estimated CTC Offer
                </span>
                <div className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-300 via-indigo-200 to-pink-300 mt-2 drop-shadow-md">
                  ₹{result.predicted_ctc_lpa} <span className="text-2xl text-slate-200">LPA</span>
                </div>
                
                {result.range && (
                  <div className="mt-4 inline-block font-mono text-xs px-4 py-1 rounded-full bg-white/10 text-slate-200 border border-white/20 backdrop-blur-md shadow-inner">
                    Confidence Interval: ₹{result.range[0]} — ₹{result.range[1]} LPA
                  </div>
                )}
              </div>

              {/* Tier Classification */}
              <div className="p-4 rounded-xl border bg-slate-900/60 border-slate-800/80 space-y-2">
                <div className="text-[11px] font-mono text-slate-400 uppercase">
                  Placement Category Tier
                </div>
                <div className={`p-2.5 rounded-lg border text-xs font-semibold ${getTier(result.predicted_ctc_lpa).color}`}>
                  {getTier(result.predicted_ctc_lpa).name}
                </div>
              </div>

              {/* Insights */}
              <div className="space-y-2 text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <Zap className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
                  <span>Aptitude scoring &gt; 80% increases placement package by an average of 15-20%.</span>
                </div>
                <div className="flex items-center gap-2">
                  <Briefcase className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                  <span>Candidates with prior internships command higher starting bands.</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-14 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-slate-500">
                <TrendingUp className="w-6 h-6" />
              </div>
              <p className="text-sm text-slate-400">
                Set CGPA and Aptitude test score, then click <br />
                <span className="text-indigo-400 font-semibold">"Estimate Expected CTC"</span>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

