"""
PlacePulse AI: Automated Test Suite
Module: tests/test_api_and_models.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add project roots
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_DIR, "src"))
sys.path.insert(0, os.path.join(PROJECT_DIR, "api"))

from main import app
from feature_engineering import clean_resume_text, analyze_skill_gaps


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["models_loaded"] is True
    assert data["version"] == "1.0.0"


def test_predict_placement_positive(client):
    payload = {
        "student_name": "Rohan Verma",
        "stream": "Computer Science",
        "cgpa": 8.8,
        "internships": 2,
        "backlogs": 0
    }
    response = client.post("/api/v1/predict/placement", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["placed"] is True
    assert data["probability"] > 80.0
    assert data["verdict"] == "High Placement Potential"
    assert data["prediction_id"] is not None


def test_predict_placement_at_risk(client):
    payload = {
        "student_name": "Vulnerable Candidate",
        "stream": "Civil",
        "cgpa": 5.8,
        "internships": 0,
        "backlogs": 1
    }
    response = client.post("/api/v1/predict/placement", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["placed"] is False
    assert data["probability"] < 50.0
    assert data["verdict"] == "Needs Immediate Support"


def test_predict_salary(client):
    payload = {
        "cgpa": 8.5,
        "aptitude_score": 82.0,
        "internships": 2,
        "stream": "Computer Science"
    }
    response = client.post("/api/v1/predict/salary", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_ctc_lpa"] > 3.0
    assert len(data["range"]) == 2
    assert data["range"][0] <= data["predicted_ctc_lpa"] <= data["range"][1]


def test_resume_screening(client):
    resume_sample = (
        "Experienced Python Developer and Machine Learning enthusiast with hands-on proficiency "
        "in Scikit-Learn, Pandas, NumPy, SQL, FastAPI, Docker, and deep learning architectures. "
        "Engineered scalable data science pipelines with 94% classification precision."
    )
    payload = {
        "candidate_name": "Ananya Sen",
        "resume_text": resume_sample,
        "target_role": "Data Science"
    }
    response = client.post("/api/v1/nlp/resume-screen", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Data Science" in data["predicted_role"] or "Python" in data["predicted_role"]
    assert len(data["matched_skills"]) > 0
    assert data["match_percentage"] > 0
    assert data["evaluation_id"] is not None


def test_at_risk_explainer(client):
    payload = {
        "stream": "Mechanical",
        "cgpa": 6.0,
        "internships": 0,
        "backlogs": 1
    }
    response = client.post("/api/v1/explain/at-risk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_at_risk"] is True
    assert data["risk_score"] > 50.0
    assert len(data["top_negative_factors"]) > 0
    assert len(data["prescriptive_action_plan"]) > 0


def test_eda_metrics(client):
    response = client.get("/api/v1/analytics/eda-metrics")
    assert response.status_code == 200
    data = response.json()
    assert "Computer Science" in data["branch_placement_rates"]
    assert "mean_lpa" in data["salary_distribution"]
    assert "CGPA" in data["correlations"]
    assert data["total_records_analyzed"] >= 1000


def test_interview_questions(client):
    payload = {
        "role": "Data Science",
        "stream": "Computer Science"
    }
    response = client.post("/api/v1/interview/questions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_found"] > 0
    assert "question" in data["questions"][0]
    assert "answer_summary" in data["questions"][0]


def test_clean_resume_text_utility():
    dirty = "Check out my profile at http://example.com/cv and email at test@domain.com! #DataScience @recruiter"
    cleaned = clean_resume_text(dirty)
    assert "http" not in cleaned
    assert "test@domain.com" not in cleaned
    assert "#" not in cleaned
    assert "@" not in cleaned


def test_rag_chat_knowledge_base_hit(client):
    """Verifies that questions in the CSV knowledge base match and receive 'Knowledge base' label."""
    payload = {
        "query": "What is the Bias-Variance tradeoff in machine learning?"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "Knowledge base"
    assert data["confidence"] > 0.20
    assert "Bias-Variance" in data["matched_question"]
    assert len(data["answer"]) > 20


def test_rag_chat_web_search_fallback(client):
    """Verifies that queries not in the CSV trigger web search with 'Web' label and links."""
    payload = {
        "query": "What are the latest 2026 tech campus placement trends in India?"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "Web"
    assert len(data["web_links"]) > 0
    assert "url" in data["web_links"][0]

