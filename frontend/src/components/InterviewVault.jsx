import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Search, 
  ChevronDown, 
  ChevronUp, 
  Code2, 
  Layers, 
  Sparkles,
  RefreshCw,
  Copy,
  Check
} from 'lucide-react';
import { getInterviewQuestions } from '../services/api';

const STREAMS = [
  'Computer Science',
  'Information Technology',
  'Electronics And Communication',
  'Mechanical',
  'Electrical',
  'Civil'
];

const ROLES = [
  'Software Engineer',
  'Data Scientist',
  'DevOps Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer'
];

export default function InterviewVault() {
  const [stream, setStream] = useState('Computer Science');
  const [role, setRole] = useState('Software Engineer');
  const [searchTerm, setSearchTerm] = useState('');
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const [copiedId, setCopiedId] = useState(null);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const res = await getInterviewQuestions(stream, role);
      if (res?.questions) {
        setQuestions(res.questions);
      }
    } catch (e) {
      console.warn('Questions fetch error', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, [stream, role]);

  const filtered = questions.filter(q => 
    q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    q.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleExpand = (idx) => {
    setExpandedId(expandedId === idx ? null : idx);
  };

  const copyToClipboard = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedId(idx);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getDifficultyColor = (diff) => {
    const d = (diff || '').toLowerCase();
    if (d === 'easy') return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
    if (d === 'hard') return 'bg-rose-500/15 text-rose-400 border-rose-500/30';
    return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
  };

  return (
    <div className="py-6 max-w-5xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-mono mb-2">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Feature 6: Technical Interview QA Recommendation Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          Technical Interview QA Vault
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Explore curated campus placement interview questions spanning DSA, System Design, Operating Systems, and Core Engineering.
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-panel p-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1 font-mono">
            Engineering Stream
          </label>
          <select
            value={stream}
            onChange={(e) => setStream(e.target.value)}
            className="input-field text-xs"
          >
            {STREAMS.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1 font-mono">
            Target Role
          </label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="input-field text-xs"
          >
            {ROLES.map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1 font-mono">
            Search Keywords
          </label>
          <div className="relative">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by topic, e.g. trees, graph, SQL..."
              className="input-field text-xs pl-8"
            />
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-2.5 top-3" />
          </div>
        </div>
      </div>

      {/* Questions List */}
      <div className="space-y-3">
        {loading ? (
          <div className="py-12 text-center text-slate-400 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-blue-400" />
            <span>Loading verified interview questions...</span>
          </div>
        ) : filtered.length > 0 ? (
          filtered.map((q, idx) => {
            const isExpanded = expandedId === idx;
            return (
              <div 
                key={idx} 
                className="glass-panel p-4 transition-all duration-150 hover:border-slate-700"
              >
                <div 
                  className="flex items-start justify-between cursor-pointer gap-4"
                  onClick={() => toggleExpand(idx)}
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getDifficultyColor(q.difficulty)}`}>
                        {q.difficulty || 'Medium'}
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                        {q.category}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">
                        {q.role} • {q.stream}
                      </span>
                    </div>
                    <h3 className="text-sm font-semibold text-slate-100 hover:text-blue-300 transition-colors">
                      {q.question}
                    </h3>
                  </div>

                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        copyToClipboard(`${q.question}\n\nAnswer Summary:\n${q.answer_summary}`, idx);
                      }}
                      className="p-1 text-slate-400 hover:text-slate-200 rounded"
                      title="Copy Q&A"
                    >
                      {copiedId === idx ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                    </button>
                    {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                  </div>
                </div>

                {isExpanded && (
                  <div className="mt-3 pt-3 border-t border-slate-800/80 text-xs text-slate-300 leading-relaxed bg-slate-900/50 p-3 rounded-lg space-y-2">
                    <div className="font-mono text-[11px] text-blue-400 font-bold uppercase">
                      Recommended Answer Summary:
                    </div>
                    <div className="whitespace-pre-wrap font-sans">
                      {q.answer_summary}
                    </div>
                  </div>
                )}
              </div>
            );
          })
        ) : (
          <div className="glass-panel p-10 text-center text-slate-400 text-xs font-mono">
            No questions matched your search criteria.
          </div>
        )}
      </div>

    </div>
  );
}
