import React, { useState } from 'react';
import { 
  AlertTriangle, 
  ShieldCheck, 
  Sparkles, 
  RefreshCw, 
  TrendingDown, 
  TrendingUp, 
  CheckCircle2, 
  ArrowRight,
  Zap,
  Lightbulb
} from 'lucide-react';
import { explainAtRisk } from '../services/api';

const STREAMS = [
  'Computer Science',
  'Information Technology',
  'Electronics And Communication',
  'Mechanical',
  'Electrical',
  'Civil'
];

export default function AtRiskExplainer({ profile, setProfile }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleExplain = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await explainAtRisk({
        stream: profile.stream,
        cgpa: profile.cgpa,
        internships: profile.internships,
        backlogs: Math.min(1, Math.max(0, profile.backlogs))
      });
      setResult(res);
    } catch (err) {
      setError(err.message || 'Failed to generate explainability report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-6 max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-mono mb-3">
          <AlertTriangle className="w-3.5 h-3.5" />
          <span>Feature 4: Transparent Explainable AI (XAI) Bottleneck Diagnostics</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          Early-Warning At-Risk Diagnostic
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Decomposes individual student risk factors and delivers transparent, prescriptive bottleneck remediation plans.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Profile Card */}
        <div className="lg:col-span-5 glass-panel p-6 space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Target Profile</span>
            <span className="text-[11px] font-mono text-slate-400">Current Inputs</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Stream:</span>
              <span className="font-semibold text-white">{profile.stream}</span>
            </div>
            <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">CGPA:</span>
              <span className="font-semibold font-mono text-blue-400">{profile.cgpa} / 10.0</span>
            </div>
            <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Internships:</span>
              <span className="font-semibold font-mono text-indigo-400">{profile.internships}</span>
            </div>
            <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Backlogs:</span>
              <span className={`font-semibold font-mono ${profile.backlogs > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                {profile.backlogs} {profile.backlogs > 0 ? '(Active)' : '(None)'}
              </span>
            </div>
          </div>

          <button
            onClick={handleExplain}
            disabled={loading}
            className="w-full btn-primary justify-center py-3 text-sm font-bold mt-2"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Decomposing Risk Drivers...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run XAI Risk Diagnostic</span>
              </>
            )}
          </button>

          {error && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
              {error}
            </div>
          )}
        </div>

        {/* Results Card */}
        <div className="lg:col-span-7 glass-panel p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Diagnostic Breakdown</span>
            <span className="text-[11px] font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
              Prescriptive Feedback
            </span>
          </div>

          {result ? (
            <div className="space-y-6">
              
              {/* Status Banner */}
              <div className={`p-4 rounded-xl border flex items-center justify-between ${
                result.is_at_risk 
                  ? 'bg-rose-500/15 border-rose-500/30 text-rose-300' 
                  : 'bg-emerald-500/15 border-emerald-500/30 text-emerald-300'
              }`}>
                <div className="flex items-center gap-3">
                  {result.is_at_risk ? (
                    <AlertTriangle className="w-6 h-6 text-rose-400 flex-shrink-0" />
                  ) : (
                    <ShieldCheck className="w-6 h-6 text-emerald-400 flex-shrink-0" />
                  )}
                  <div>
                    <div className="font-bold text-sm">
                      {result.is_at_risk ? 'Candidate Flagged: At-Risk' : 'Candidate Status: Low Risk'}
                    </div>
                    <div className="text-xs opacity-90 mt-0.5">{result.verdict}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs font-mono uppercase opacity-75">Risk Index</div>
                  <div className="text-lg font-mono font-extrabold">{result.risk_score} / 100</div>
                </div>
              </div>

              {/* Negative Drivers */}
              {result.top_negative_factors?.length > 0 && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-rose-400 uppercase font-mono">
                    <TrendingDown className="w-4 h-4" />
                    <span>Identified Risk Drivers & Penalties</span>
                  </div>
                  <div className="space-y-2">
                    {result.top_negative_factors.map((item, idx) => (
                      <div key={idx} className="p-3 rounded-lg bg-slate-900/60 border border-rose-500/20 text-xs space-y-1">
                        <div className="flex justify-between font-semibold text-slate-200">
                          <span>{item.factor}</span>
                          <span className="text-rose-400 font-mono">-{item.penalty_pct}% Penalty</span>
                        </div>
                        <p className="text-slate-400">{item.description}</p>
                        <p className="text-blue-300 text-[11px] pt-1">💡 {item.recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Positive Factors */}
              {result.positive_factors?.length > 0 && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 uppercase font-mono">
                    <TrendingUp className="w-4 h-4" />
                    <span>Strengths & Catalysts</span>
                  </div>
                  <div className="space-y-2">
                    {result.positive_factors.map((item, idx) => (
                      <div key={idx} className="p-3 rounded-lg bg-slate-900/60 border border-emerald-500/20 text-xs space-y-1">
                        <div className="flex justify-between font-semibold text-slate-200">
                          <span>{item.factor}</span>
                          <span className="text-emerald-400 font-mono">+{item.penalty_pct}% Boost</span>
                        </div>
                        <p className="text-slate-400">{item.description}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Plan */}
              {result.prescriptive_action_plan?.length > 0 && (
                <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-amber-400 uppercase font-mono">
                    <Lightbulb className="w-4 h-4" />
                    <span>Prescriptive Action Roadmap</span>
                  </div>
                  <ul className="space-y-1.5 text-xs text-slate-300">
                    {result.prescriptive_action_plan.map((act, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-blue-400 font-mono font-bold">{i + 1}.</span>
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

            </div>
          ) : (
            <div className="py-14 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-slate-500">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <p className="text-sm text-slate-400">
                Click <span className="text-amber-400 font-semibold">"Run XAI Risk Diagnostic"</span> to <br />
                evaluate risk bottlenecks and obtain actionable recommendations.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

