"""
CampusNova AI: Asynchronous FastAPI Placement Intelligence Microservice
Module: api/main.py
Author: CampusNova AI Team
License: Approved Production Blueprint - v1.0.0
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from contextlib import asynccontextmanager
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add src and api to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
DATA_DIR = os.path.join(CURRENT_DIR, "..", "data")
MODELS_DIR = os.path.join(CURRENT_DIR, "..", "models")
FRONTEND_DIST = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "frontend", "dist"))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from feature_engineering import (
    clean_resume_text,
    analyze_skill_gaps,
    STREAM_KEYS,
    TECH_SKILL_TAXONOMY
)
from explainability import PlacementExplainer
from rag_chat_engine import RAGChatEngine
from database import (
    init_database,
    log_placement_prediction,
    log_resume_evaluation,
    get_recent_predictions,
    get_db_connection
)
from schemas import (
    PlacementPredictionRequest, PlacementPredictionResponse,
    SalaryPredictionRequest, SalaryPredictionResponse,
    ResumeScreenRequest, ResumeScreenResponse,
    AtRiskExplainerRequest, AtRiskExplainerResponse,
    InterviewQuestionRequest, InterviewQuestionResponse, InterviewQuestionItem,
    EDAMetricsResponse, HealthResponse,
    ChatQueryRequest, ChatQueryResponse, WebLinkItem
)

# Global model state cache
ml_models: Dict[str, Any] = {}


def load_all_artifacts():
    """Initializes database and loads serialized ML models into cache."""
    init_database()

    # Load Classification Pipeline
    clf_pipe_path = os.path.join(MODELS_DIR, "placement_pipeline.joblib")
    if os.path.exists(clf_pipe_path):
        ml_models["placement_pipeline"] = joblib.load(clf_pipe_path)

    # Load Salary Regression Pipeline
    reg_pipe_path = os.path.join(MODELS_DIR, "salary_pipeline.joblib")
    if os.path.exists(reg_pipe_path):
        ml_models["salary_pipeline"] = joblib.load(reg_pipe_path)

    # Load Resume NLP Artifacts
    nlp_path = os.path.join(MODELS_DIR, "resume_classifier.joblib")
    tfidf_path = os.path.join(MODELS_DIR, "resume_tfidf.joblib")
    label_path = os.path.join(MODELS_DIR, "resume_label_encoder.joblib")
    if os.path.exists(nlp_path) and os.path.exists(tfidf_path) and os.path.exists(label_path):
        ml_models["resume_classifier"] = joblib.load(nlp_path)
        ml_models["resume_tfidf"] = joblib.load(tfidf_path)
        ml_models["resume_label_encoder"] = joblib.load(label_path)

    # Load Explainability Engine
    try:
        ml_models["explainer"] = PlacementExplainer()
    except Exception as e:
        print(f"Warning: Could not initialize explainer: {e}")

    # Load Interview QA Dataset
    qa_path = os.path.join(DATA_DIR, "raw", "technical_interview_qa.csv")
    if os.path.exists(qa_path):
        ml_models["interview_qa"] = pd.read_csv(qa_path)
    else:
        ml_models["interview_qa"] = pd.DataFrame()

    # Load Hybrid RAG & Web Search Engine
    try:
        ml_models["rag_chat"] = RAGChatEngine(qa_csv_path=qa_path)
    except Exception as e:
        print(f"Warning: Could not initialize RAGChatEngine: {e}")


# Eager load artifacts on startup
load_all_artifacts()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: ensures artifacts are loaded."""
    if not ml_models:
        load_all_artifacts()
    yield
    ml_models.clear()


app = FastAPI(
    title="CampusNova AI Microservice",
    description="B.Tech Campus Placement Predictive Intelligence & Data Science Platform REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for frontend clients (Streamlit, React, Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount compiled React Liquid Glass static assets
assets_dir = os.path.join(FRONTEND_DIST, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/api/v1/health", response_model=HealthResponse, tags=["System Health"])
async def health_check():
    """Health check endpoint: verifies service status and active serialized models."""
    is_ready = bool(
        "placement_pipeline" in ml_models and
        "salary_pipeline" in ml_models and
        "resume_classifier" in ml_models
    )

    clf_name = type(ml_models.get("placement_pipeline")).__name__ if "placement_pipeline" in ml_models else "None"
    reg_name = type(ml_models.get("salary_pipeline")).__name__ if "salary_pipeline" in ml_models else "None"
    nlp_name = type(ml_models.get("resume_classifier")).__name__ if "resume_classifier" in ml_models else "None"

    return HealthResponse(
        status="ok",
        models_loaded=is_ready,
        version="1.0.0",
        active_classifier=clf_name,
        active_regressor=reg_name,
        active_nlp_model=nlp_name
    )


@app.post("/api/v1/predict/placement", response_model=PlacementPredictionResponse, tags=["Inference"])
async def predict_placement(req: PlacementPredictionRequest):
    """
    Feature 1: B.Tech Placement Probability Classifier.
    Predicts binary placement potential (Offer Likelihood) and outputs exact probability score.
    """
    if "placement_pipeline" not in ml_models:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Placement ML model pipeline is not loaded. Train models before inference."
        )

    pipeline = ml_models["placement_pipeline"]

    # Transform request into standard DataFrame matching training schema
    df_sample = pd.DataFrame([{
        "CGPA": float(req.cgpa),
        "CGPA_x_Intern": float(req.cgpa) * (int(req.internships) + 1),
        "Stream": str(req.stream),
        "Internships": int(req.internships),
        "HistoryOfBacklogs": int(req.backlogs)
    }])

    # Inference
    if hasattr(pipeline, "predict_proba"):
        proba = float(pipeline.predict_proba(df_sample)[0, 1])
    elif hasattr(pipeline, "decision_function"):
        score = float(pipeline.decision_function(df_sample)[0])
        proba = float(1.0 / (1.0 + np.exp(-score)))
    else:
        proba = float(pipeline.predict(df_sample)[0])

    is_placed = bool(proba >= 0.50)
    verdict = "High Placement Potential" if is_placed else "Needs Immediate Support"
    confidence = "High" if abs(proba - 0.5) > 0.25 else "Moderate"

    # Persist prediction in SQLite
    pred_id = log_placement_prediction(
        stream=req.stream,
        cgpa=req.cgpa,
        internships=req.internships,
        backlogs=req.backlogs,
        predicted_placement=is_placed,
        placement_probability=round(proba, 4),
        student_name=req.student_name,
        model_version="v1.0.0"
    )

    return PlacementPredictionResponse(
        placed=is_placed,
        probability=round(proba * 100.0, 2),
        confidence=confidence,
        verdict=verdict,
        stream=req.stream,
        cgpa=req.cgpa,
        internships=req.internships,
        backlogs=req.backlogs,
        prediction_id=pred_id
    )


@app.post("/api/v1/predict/salary", response_model=SalaryPredictionResponse, tags=["Inference"])
async def predict_salary(req: SalaryPredictionRequest):
    """
    Feature 2: Expected CTC / Salary Package Regressor.
    Estimates compensation package (in LPA) based on degree performance, aptitude scores, and internships.
    """
    if "salary_pipeline" not in ml_models:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Salary regressor model pipeline is not loaded."
        )

    pipeline = ml_models["salary_pipeline"]

    degree_pct = req.cgpa * 9.5
    workex_bin = 1 if req.internships > 0 else 0
    df_sample = pd.DataFrame([{
        "degree_p": float(degree_pct),
        "etest_p": float(req.aptitude_score),
        "workex_binary": int(workex_bin)
    }])

    pred_lpa = float(pipeline.predict(df_sample)[0])
    pred_lpa = max(2.5, round(pred_lpa, 2))
    margin = 0.55
    min_range = max(2.2, round(pred_lpa - margin, 2))
    max_range = round(pred_lpa + margin, 2)

    return SalaryPredictionResponse(
        predicted_ctc_lpa=pred_lpa,
        range=[min_range, max_range],
        model_name="Ridge Regression (Pipeline)",
        currency="INR (LPA)"
    )


@app.post("/api/v1/nlp/resume-screen", response_model=ResumeScreenResponse, tags=["NLP & Resume"])
async def screen_resume(req: ResumeScreenRequest):
    """
    Feature 3: Technical Resume Domain Classification & Skill-Gap NLP Engine.
    Maps candidate resume into 25+ tech categories and returns matched and missing competencies.
    """
    if "resume_classifier" not in ml_models or "resume_tfidf" not in ml_models or "resume_label_encoder" not in ml_models:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Resume NLP models are not loaded."
        )

    classifier = ml_models["resume_classifier"]
    tfidf = ml_models["resume_tfidf"]
    label_encoder = ml_models["resume_label_encoder"]

    cleaned = clean_resume_text(req.resume_text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="Resume text is empty after cleaning.")

    X_vec = tfidf.transform([cleaned])

    # Predict category
    predicted_idx = int(classifier.predict(X_vec)[0])
    predicted_role = str(label_encoder.inverse_transform([predicted_idx])[0])

    # Softmax confidence
    confidence = 0.95
    if hasattr(classifier, "decision_function"):
        scores = classifier.decision_function(X_vec)
        exp_scores = np.exp(scores - np.max(scores))
        confidence = round(float(np.max(exp_scores / np.sum(exp_scores))), 4)

    # Skill-Gap Analysis against exact domain taxonomy
    target_domain = req.target_role if req.target_role else predicted_role
    gap_result = analyze_skill_gaps(req.resume_text, target_domain)

    # Persist in SQLite
    eval_id = log_resume_evaluation(
        raw_resume_snippet=req.resume_text,
        predicted_category=predicted_role,
        confidence_score=confidence,
        matched_skills=gap_result["matched_skills"],
        missing_skills=gap_result["missing_skills"],
        candidate_name=req.candidate_name
    )

    return ResumeScreenResponse(
        predicted_role=predicted_role,
        confidence=confidence,
        matched_skills=gap_result["matched_skills"],
        missing_skills=gap_result["missing_skills"],
        match_percentage=gap_result["match_percentage"],
        total_skills_evaluated=gap_result["total_skills_evaluated"],
        evaluation_id=eval_id
    )


@app.post("/api/v1/explain/at-risk", response_model=AtRiskExplainerResponse, tags=["Explainable AI"])
async def explain_at_risk(req: AtRiskExplainerRequest):
    """
    Feature 4: Early-Warning At-Risk Explainer (Explainable AI).
    Decomposes risk drivers and delivers transparent, prescriptive bottleneck diagnostics.
    """
    if "explainer" not in ml_models:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Explainability engine is not initialized."
        )

    explainer: PlacementExplainer = ml_models["explainer"]
    res = explainer.explain_profile(req.stream, req.cgpa, req.internships, req.backlogs)
    return AtRiskExplainerResponse(**res)


@app.get("/api/v1/analytics/eda-metrics", response_model=EDAMetricsResponse, tags=["Analytics"])
async def get_eda_metrics():
    """
    Feature 5: Exploratory Data Analysis & Aggregate Campus Placement Metrics.
    Returns branch placement rates, salary quartiles, and feature correlations.
    """
    proc_csv = os.path.join(DATA_DIR, "processed", "college_placement_processed.csv")
    salary_csv = os.path.join(DATA_DIR, "processed", "salary_placed_processed.csv")

    if not os.path.exists(proc_csv) or not os.path.exists(salary_csv):
        raise HTTPException(status_code=404, detail="Processed dataset files not found.")

    df_col = pd.read_csv(proc_csv)
    df_sal = pd.read_csv(salary_csv)

    branch_rates = (
        df_col.groupby("Stream")["PlacedOrNot"]
        .mean()
        .round(4)
        .to_dict()
    )

    salary_stats = {
        "mean_lpa": round(float(df_sal["salary_lpa"].mean()), 2),
        "median_lpa": round(float(df_sal["salary_lpa"].median()), 2),
        "min_lpa": round(float(df_sal["salary_lpa"].min()), 2),
        "max_lpa": round(float(df_sal["salary_lpa"].max()), 2),
        "p25_lpa": round(float(df_sal["salary_lpa"].quantile(0.25)), 2),
        "p75_lpa": round(float(df_sal["salary_lpa"].quantile(0.75)), 2)
    }

    num_cols = ["CGPA", "Internships", "HistoryOfBacklogs", "CGPA_Internship_Interaction", "PlacedOrNot"]
    corr_series = df_col[num_cols].corr()["PlacedOrNot"].drop("PlacedOrNot").round(4).to_dict()

    return EDAMetricsResponse(
        branch_placement_rates=branch_rates,
        salary_distribution=salary_stats,
        correlations=corr_series,
        total_records_analyzed=len(df_col)
    )


@app.post("/api/v1/interview/questions", response_model=InterviewQuestionResponse, tags=["Interview Prep"])
async def get_interview_questions(req: InterviewQuestionRequest):
    """
    Feature 6: Technical Interview QA Recommendation Engine.
    Filters verified DSA and domain engineering interview questions by role and engineering stream.
    """
    df_qa: pd.DataFrame = ml_models.get("interview_qa", pd.DataFrame())
    if df_qa.empty:
        raise HTTPException(status_code=404, detail="Technical interview QA repository is empty.")

    mask = (df_qa["role"].str.contains(req.role, case=False, na=False)) | (df_qa["stream"].str.contains(req.stream, case=False, na=False))
    matched_df = df_qa[mask]

    if matched_df.empty:
        matched_df = df_qa.head(5)

    items = []
    for _, row in matched_df.iterrows():
        items.append(InterviewQuestionItem(
            question=row["question"],
            category=row["category"],
            difficulty=row["difficulty"],
            answer_summary=row["answer_summary"],
            role=row["role"],
            stream=row["stream"]
        ))

    return InterviewQuestionResponse(total_found=len(items), questions=items)


@app.get("/api/v1/predictions/history", tags=["Database Logs"])
async def get_history(limit: int = 20):
    """Fetches recent logged predictions from SQLite."""
    rows = get_recent_predictions(limit=limit)
    return {"count": len(rows), "records": rows}


@app.get("/api/v1/benchmarks", tags=["Model Registry"])
async def get_benchmarks():
    """Retrieves all benchmark metrics registered in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model_benchmark_registry ORDER BY task_type, id")
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"total_models": len(records), "benchmarks": records}


# -------------------------------------------------------------
# 7. RAG & Web Search Hybrid Placement Assistant
# -------------------------------------------------------------
@app.post("/api/v1/chat", response_model=ChatQueryResponse, tags=["AI Mentor Chat (RAG + Web)"])
@app.post("/chat", response_model=ChatQueryResponse, tags=["AI Mentor Chat (RAG + Web)"], include_in_schema=False)
async def chat_with_mentor(req: ChatQueryRequest):
    """
    RAG & Web Search Hybrid Placement Assistant:
    Student types question in chat
            ↓
    FastAPI /chat endpoint
            ↓
    Search knowledge base (CSV) for similar questions
            ↓
       Good match?
       ├── Yes → LLM answers from CSV entries   → label: 'Knowledge base'
       └── No  → Search the web → LLM answers   → label: 'Web' + links
            ↓
    Answer shown in chat, with source label
    """
    engine: Optional[RAGChatEngine] = ml_models.get("rag_chat")
    if not engine:
        engine = RAGChatEngine()
        ml_models["rag_chat"] = engine

    res = engine.chat(query=req.query, api_key=req.api_key)

    return ChatQueryResponse(
        query=res["query"],
        answer=res["answer"],
        source=res["source"],
        confidence=res["confidence"],
        matched_question=res.get("matched_question"),
        category=res.get("category"),
        role=res.get("role"),
        web_links=[WebLinkItem(title=item["title"], url=item["url"]) for item in res.get("web_links", [])]
    )

# -------------------------------------------------------------
# 8. Single Unified Full-Stack SPA Serving (Render Web Portal)
# -------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def serve_spa_root():
    """Serves compiled React Liquid Glass SPA on root URL."""
    index_file = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "ok", "message": "CampusNova AI Microservice API is running. Build frontend/dist to view UI."}


@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa_catch_all(full_path: str):
    """Fallback catch-all route for React client-side routing and static assets."""
    if full_path.startswith("api/") or full_path in ["docs", "redoc", "openapi.json", "chat"]:
        raise HTTPException(status_code=404, detail="API route not found")

    file_candidate = os.path.join(FRONTEND_DIST, full_path)
    if os.path.exists(file_candidate) and os.path.isfile(file_candidate):
        return FileResponse(file_candidate)

    index_file = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)

    raise HTTPException(status_code=404, detail="Page not found")

