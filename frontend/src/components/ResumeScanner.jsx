import React, { useState } from 'react';
import { 
  FileText, 
  Sparkles, 
  CheckCircle2, 
  XCircle, 
  RefreshCw, 
  AlertCircle,
  Copy,
  Check,
  Target
} from 'lucide-react';
import { screenResume } from '../services/api';

const SAMPLE_RESUMES = {
  fullstack: {
    title: 'Full Stack Engineer',
    text: `Rahul Sharma | Full Stack Software Engineer | rahul@example.com
EDUCATION: B.Tech Computer Science and Engineering, CGPA: 8.4
SKILLS: JavaScript, TypeScript, React, Node.js, Express, MongoDB, PostgreSQL, REST APIs, Git, Docker, HTML5, CSS3, TailwindCSS, Jest.
EXPERIENCE: Full Stack Intern at TechCorp (6 months). Built scalable microservices with Node.js and interactive dashboards in React. Integrated Redis caching and JWT authentication.
PROJECTS: 
1. Real-Time Collaboration Hub: WebSockets, React, MongoDB, Node.js. Handled 500+ concurrent connections.
2. E-Commerce Microservices API: Dockerized backend with PostgreSQL and Stripe checkout integration.`
  },
  datascientist: {
    title: 'Data Scientist / ML',
    text: `Priya Patel | Data Science & Machine Learning Specialist
EDUCATION: B.Tech Information Technology, CGPA: 8.8
SKILLS: Python, SQL, Pandas, NumPy, Scikit-Learn, PyTorch, TensorFlow, Data Visualization, Matplotlib, Seaborn, Machine Learning, Deep Learning, NLP, Docker.
EXPERIENCE: ML Research Intern at DataPulse Labs. Developed classification pipelines with 94% precision. Performed EDA on 500k+ customer records.
PROJECTS:
1. Customer Churn Prediction Engine: XGBoost, Scikit-Learn, Flask API, Docker.
2. Automated Resume Parser: SpaCy NLP, TF-IDF vectorization, named entity recognition.`
  },
  devops: {
    title: 'DevOps & Cloud Engineer',
    text: `Ankit Verma | DevOps & Cloud Infrastructure Engineer
EDUCATION: B.Tech Electronics and Communication, CGPA: 7.9
SKILLS: Linux, Docker, Kubernetes, AWS (EC2, S3, IAM, EKS), CI/CD, GitHub Actions, Terraform, Bash Scripting, Prometheus, Grafana, Nginx.
EXPERIENCE: Cloud Intern at InfraStack. Configured automated CI/CD pipelines deploying Docker containers to Kubernetes clusters. Managed infrastructure as code via Terraform.`
  }
};

const COMMON_DOMAINS = [
  'Auto-Detect from Resume',
  'Software Engineer',
  'Data Scientist',
  'DevOps Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'Machine Learning Engineer',
  'Database Administrator',
  'Cloud Engineer'
];

export default function ResumeScanner() {
  const [resumeText, setResumeText] = useState(SAMPLE_RESUMES.fullstack.text);
  const [targetRole, setTargetRole] = useState('Auto-Detect from Resume');
  const [candidateName, setCandidateName] = useState('Rahul Sharma');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async () => {
    if (!resumeText.trim()) {
      setError('Please paste or load a resume snippet.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const rolePayload = targetRole === 'Auto-Detect from Resume' ? null : targetRole;
      const res = await screenResume({
        resume_text: resumeText,
        target_role: rolePayload,
        candidate_name: candidateName
      });
      setResult(res);
    } catch (err) {
      setError(err.message || 'Failed to analyze resume');
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (key) => {
    setResumeText(SAMPLE_RESUMES[key].text);
    setCandidateName(SAMPLE_RESUMES[key].text.split('|')[0].trim());
    setResult(null);
  };

  return (
    <div className="py-6 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-pink-500/10 border border-pink-500/20 text-pink-400 text-xs font-mono mb-3">
          <FileText className="w-3.5 h-3.5" />
          <span>Feature 3: LinearSVC NLP Resume Screening & Skill Gap Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          Technical Resume Screener & Skill-Gap NLP
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Parses candidate resume text across 1,500 TF-IDF features to classify tech roles and benchmark competencies against domain taxonomies.
        </p>
      </div>

      {/* Preset Buttons */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-400 font-mono">Load Sample Profile:</span>
        <button
          onClick={() => loadPreset('fullstack')}
          className="px-3 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-200 border border-slate-700/60 font-medium transition-colors"
        >
          Full Stack Engineer
        </button>
        <button
          onClick={() => loadPreset('datascientist')}
          className="px-3 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-200 border border-slate-700/60 font-medium transition-colors"
        >
          Data Scientist / ML
        </button>
        <button
          onClick={() => loadPreset('devops')}
          className="px-3 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-200 border border-slate-700/60 font-medium transition-colors"
        >
          DevOps & Cloud
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Input Area */}
        <div className="lg:col-span-6 glass-panel p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Resume Content</span>
            <span className="text-[11px] font-mono text-slate-400">Plaintext / Markdown</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1 font-mono">
                Candidate Name
              </label>
              <input
                type="text"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
                className="input-field text-xs"
                placeholder="Candidate Name"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1 font-mono">
                Benchmark Role
              </label>
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="input-field text-xs"
              >
                {COMMON_DOMAINS.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <textarea
              rows={12}
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              className="input-field font-mono text-xs leading-relaxed"
              placeholder="Paste raw resume or technical bio here..."
            />
          </div>

          <button
            onClick={handleScan}
            disabled={loading}
            className="w-full btn-primary justify-center py-3 text-sm font-bold"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running TF-IDF & LinearSVC Classifier...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Analyze Resume Competencies</span>
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

        {/* Right Output Area */}
        <div className="lg:col-span-6 glass-panel p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-white font-semibold text-sm">Competency Assessment</span>
            <span className="text-[11px] font-mono text-pink-400 bg-pink-500/10 px-2 py-0.5 rounded border border-pink-500/20">
              NLP Taxonomy
            </span>
          </div>

          {result ? (
            <div className="space-y-6">
              
              {/* Domain Classification Banner */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-blue-950/40 to-indigo-950/40 border border-blue-500/30">
                <div className="text-[10px] font-mono text-blue-300 uppercase tracking-wider">
                  Predicted Technical Domain
                </div>
                <div className="text-xl font-bold text-white mt-1 flex items-center justify-between">
                  <span>{result.predicted_role}</span>
                  <span className="text-xs font-mono font-medium px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30">
                    {(result.confidence * 100).toFixed(1)}% Confidence
                  </span>
                </div>
              </div>

              {/* Match Percentage */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-semibold text-slate-300 font-mono uppercase">
                    Taxonomy Match Index
                  </span>
                  <span className="font-mono font-bold text-emerald-400">
                    {result.match_percentage}% ({result.matched_skills.length} / {result.total_skills_evaluated} Skills)
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2.5 overflow-hidden border border-slate-800">
                  <div 
                    className="bg-gradient-to-r from-emerald-500 to-teal-400 h-2.5 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, result.match_percentage)}%` }}
                  ></div>
                </div>
              </div>

              {/* Matched Skills */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 uppercase font-mono">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Verified Present Competencies ({result.matched_skills.length})</span>
                </div>
                <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto p-1">
                  {result.matched_skills.length > 0 ? (
                    result.matched_skills.map((skill, i) => (
                      <span 
                        key={i} 
                        className="px-2.5 py-1 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs font-mono"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-slate-500 italic">No recognized taxonomy skills detected</span>
                  )}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs font-semibold text-rose-400 uppercase font-mono">
                  <XCircle className="w-4 h-4" />
                  <span>Identified Skill Gaps ({result.missing_skills.length})</span>
                </div>
                <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto p-1">
                  {result.missing_skills.length > 0 ? (
                    result.missing_skills.map((skill, i) => (
                      <span 
                        key={i} 
                        className="px-2.5 py-1 rounded-lg bg-rose-500/10 border border-rose-500/25 text-rose-300 text-xs font-mono"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-emerald-400 font-medium">No major missing competencies detected!</span>
                  )}
                </div>
              </div>

            </div>
          ) : (
            <div className="py-14 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-slate-500">
                <Target className="w-6 h-6" />
              </div>
              <p className="text-sm text-slate-400">
                Paste resume snippet on the left and click <br />
                <span className="text-pink-400 font-semibold">"Analyze Resume Competencies"</span>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
