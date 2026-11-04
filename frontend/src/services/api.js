/**
 * CampusNova AI - API Client Service
 * Connects directly to Render FastAPI Microservice
 */

const getBaseUrl = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  if (typeof window !== 'undefined' && window.location.origin) {
    // If running on Vite dev port 5173, point to production Render backend
    if (window.location.port === '5173') {
      return 'https://campus-nova-purr.onrender.com';
    }
    // On Render (same origin), relative path works seamlessly
    return '';
  }
  return 'https://campus-nova-purr.onrender.com';
};

export const API_BASE_URL = getBaseUrl();

/**
 * Health check
 */
export async function getHealthStatus() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/health`, { method: 'GET' });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Backend health check error:', err);
    return { status: 'error', message: err.message };
  }
}

/**
 * Placement Probability Prediction
 */
export async function predictPlacement(data) {
  const res = await fetch(`${API_BASE_URL}/api/v1/predict/placement`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      stream: data.stream,
      cgpa: parseFloat(data.cgpa),
      internships: parseInt(data.internships, 10),
      backlogs: parseInt(data.backlogs, 10),
      student_name: data.student_name || 'Engineering Student'
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Prediction failed with status ${res.status}`);
  }
  return await res.json();
}

/**
 * Expected CTC Salary Prediction
 */
export async function predictSalary(data) {
  const res = await fetch(`${API_BASE_URL}/api/v1/predict/salary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      cgpa: parseFloat(data.cgpa),
      internships: parseInt(data.internships, 10),
      aptitude_score: parseFloat(data.aptitude_score || 75.0)
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Salary estimation failed with status ${res.status}`);
  }
  return await res.json();
}

/**
 * Technical Resume Screening & Skill Gap NLP
 */
export async function screenResume(data) {
  const res = await fetch(`${API_BASE_URL}/api/v1/nlp/resume-screen`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_text: data.resume_text,
      target_role: data.target_role || null,
      candidate_name: data.candidate_name || 'Candidate'
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Resume screening failed with status ${res.status}`);
  }
  return await res.json();
}

/**
 * Early-Warning At-Risk Explainability (XAI)
 */
export async function explainAtRisk(data) {
  const res = await fetch(`${API_BASE_URL}/api/v1/explain/at-risk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      stream: data.stream,
      cgpa: parseFloat(data.cgpa),
      internships: parseInt(data.internships, 10),
      backlogs: parseInt(data.backlogs, 10)
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Explainability analysis failed with status ${res.status}`);
  }
  return await res.json();
}

/**
 * Hybrid RAG & Live Web Placement Assistant Chat
 */
export async function sendChatMessage(query, apiKey = null) {
  const res = await fetch(`${API_BASE_URL}/api/v1/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: query,
      api_key: apiKey
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Chat query failed with status ${res.status}`);
  }
  return await res.json();
}

/**
 * Technical Interview QA Repository
 */
export async function getInterviewQuestions(stream = 'Computer Science', role = 'Software Engineer') {
  const res = await fetch(`${API_BASE_URL}/api/v1/interview/questions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      stream: stream,
      role: role
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch interview questions (${res.status})`);
  }
  return await res.json();
}

/**
 * Benchmark Registry
 */
export async function getBenchmarks() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/benchmarks`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Could not fetch benchmarks:', err);
    return { benchmarks: [] };
  }
}

/**
 * Prediction History
 */
export async function getPredictionHistory(limit = 20) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/predictions/history?limit=${limit}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Could not fetch history:', err);
    return { records: [] };
  }
}

/**
 * EDA Metrics
 */
export async function getEdaMetrics() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/analytics/eda-metrics`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Could not fetch EDA metrics:', err);
    return null;
  }
}
