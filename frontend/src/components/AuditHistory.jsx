import React, { useState, useEffect } from 'react';
import { 
  History, 
  RefreshCw, 
  CheckCircle2, 
  AlertCircle, 
  Database,
  Calendar
} from 'lucide-react';
import { getPredictionHistory } from '../services/api';

export default function AuditHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await getPredictionHistory(30);
      if (res?.records) {
        setHistory(res.records);
      }
    } catch (e) {
      console.warn('History fetch error', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="py-6 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-mono mb-2">
            <History className="w-3.5 h-3.5" />
            <span>SQLite Prediction Audit Log</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            Live Prediction Audit History
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time telemetry and immutable audit trails stored in production database.
          </p>
        </div>

        <button
          onClick={fetchHistory}
          disabled={loading}
          className="btn-secondary text-xs"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Audit Logs</span>
        </button>
      </div>

      <div className="glass-panel p-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800 font-mono uppercase text-[11px]">
              <tr>
                <th className="px-4 py-3">Audit ID</th>
                <th className="px-4 py-3">Candidate / Student</th>
                <th className="px-4 py-3">Stream</th>
                <th className="px-4 py-3">CGPA</th>
                <th className="px-4 py-3">Internships</th>
                <th className="px-4 py-3">Backlogs</th>
                <th className="px-4 py-3">Probability</th>
                <th className="px-4 py-3 text-right">Verdict</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {history.length > 0 ? (
                history.map((row, idx) => {
                  const isPlaced = row.predicted_placement === 1 || row.predicted_placement === true;
                  const probPct = (row.placement_probability * 100).toFixed(1);
                  return (
                    <tr key={idx} className="hover:bg-slate-900/40 transition-colors">
                      <td className="px-4 py-3 text-slate-500">#{row.id}</td>
                      <td className="px-4 py-3 font-sans font-semibold text-slate-100">
                        {row.student_name || 'Engineering Student'}
                      </td>
                      <td className="px-4 py-3 font-sans text-slate-300">{row.stream}</td>
                      <td className="px-4 py-3 font-bold text-blue-400">{row.cgpa}</td>
                      <td className="px-4 py-3">{row.internships}</td>
                      <td className="px-4 py-3">
                        <span className={row.backlogs > 0 ? 'text-rose-400 font-bold' : 'text-slate-400'}>
                          {row.backlogs}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-bold text-slate-100">
                        {probPct}%
                      </td>
                      <td className="px-4 py-3 text-right">
                        {isPlaced ? (
                          <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                            <CheckCircle2 className="w-3 h-3" />
                            <span>Placed</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30">
                            <AlertCircle className="w-3 h-3" />
                            <span>At-Risk</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="8" className="px-4 py-8 text-center text-slate-500">
                    {loading ? 'Fetching audit records...' : 'No prediction audit logs found yet.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

