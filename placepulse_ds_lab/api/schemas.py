"""
PlacePulse AI: Pydantic v2 Request & Response Data Schemas
Module: api/schemas.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# 1. Placement Probability
class PlacementPredictionRequest(BaseModel):
    student_name: Optional[str] = Field(default=None, description="Optional name of the student candidate")
    stream: str = Field(..., description="Engineering Branch, e.g. 'Computer Science', 'Information Technology', 'Mechanical'")
    cgpa: float = Field(..., ge=0.0, le=10.0, description="Cumulative Grade Point Average (0.0 to 10.0)")
    internships: int = Field(default=0, ge=0, le=10, description="Total completed internships count")
    backlogs: int = Field(default=0, ge=0, le=1, description="History of backlogs (0 = Clear, 1 = Previous Backlogs)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "student_name": "Aarav Sharma",
                "stream": "Computer Science",
                "cgpa": 8.45,
                "internships": 2,
                "backlogs": 0
            }
        }
    }


class PlacementPredictionResponse(BaseModel):
    placed: bool
    probability: float
    confidence: str
    verdict: str
    stream: str
    cgpa: float
    internships: int
    backlogs: int
    prediction_id: Optional[int] = None


# 2. Salary Regression
class SalaryPredictionRequest(BaseModel):
    cgpa: float = Field(..., ge=0.0, le=10.0, description="Student CGPA (0.0 to 10.0)")
    aptitude_score: float = Field(..., ge=0.0, le=100.0, description="Campus Aptitude / E-Test Score (0 to 100)")
    internships: int = Field(default=0, ge=0, description="Internship count or work experience indicator")
    stream: Optional[str] = Field(default="Computer Science", description="Engineering Stream")

    model_config = {
        "json_schema_extra": {
            "example": {
                "cgpa": 8.2,
                "aptitude_score": 78.5,
                "internships": 1,
                "stream": "Information Technology"
            }
        }
    }


class SalaryPredictionResponse(BaseModel):
    predicted_ctc_lpa: float
    range: List[float]
    model_name: str
    currency: str = "INR (LPA)"


# 3. Resume Screen & NLP
class ResumeScreenRequest(BaseModel):
    resume_text: str = Field(..., min_length=20, description="Raw plain text or extracted content from candidate resume")
    candidate_name: Optional[str] = Field(default=None, description="Candidate name")
    target_role: Optional[str] = Field(default=None, description="Optional target role for tailored skill-gap analysis")

    model_config = {
        "json_schema_extra": {
            "example": {
                "candidate_name": "Priya Nair",
                "resume_text": "Experienced Python Developer with strong proficiency in FastAPI, Django, PostgreSQL, Docker, and REST APIs. Built microservices handling 50k daily active requests.",
                "target_role": "Python Developer"
            }
        }
    }


class ResumeScreenResponse(BaseModel):
    predicted_role: str
    confidence: float
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float
    total_skills_evaluated: int
    evaluation_id: Optional[int] = None


# 4. Explainable AI / At-Risk Explainer
class AtRiskExplainerRequest(BaseModel):
    stream: str = Field(..., description="Engineering stream")
    cgpa: float = Field(..., ge=0.0, le=10.0)
    internships: int = Field(default=0, ge=0)
    backlogs: int = Field(default=0, ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "stream": "Mechanical",
                "cgpa": 6.2,
                "internships": 0,
                "backlogs": 1
            }
        }
    }


class AtRiskFactorItem(BaseModel):
    factor: str
    impact_type: str
    penalty_pct: float
    description: str
    recommendation: str


class AtRiskExplainerResponse(BaseModel):
    is_at_risk: bool
    risk_score: float
    placement_probability: float
    confidence: str
    verdict: str
    top_negative_factors: List[AtRiskFactorItem]
    positive_factors: List[AtRiskFactorItem]
    prescriptive_action_plan: List[str]
    simulation_potentials: Dict[str, float]


# 5. Interview Questions
class InterviewQuestionRequest(BaseModel):
    role: str = Field(default="Data Science", description="Job domain or role, e.g. 'Data Science', 'Java Developer'")
    stream: Optional[str] = Field(default="Computer Science", description="Engineering Stream")


class InterviewQuestionItem(BaseModel):
    question: str
    category: str
    difficulty: str
    answer_summary: str
    role: str
    stream: str


class InterviewQuestionResponse(BaseModel):
    total_found: int
    questions: List[InterviewQuestionItem]


# 6. Analytics & Health
class EDAMetricsResponse(BaseModel):
    branch_placement_rates: Dict[str, float]
    salary_distribution: Dict[str, Any]
    correlations: Dict[str, float]
    total_records_analyzed: int


class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    version: str
    active_classifier: str
    active_regressor: str
    active_nlp_model: str


# 7. RAG & Web Search Hybrid Assistant
class WebLinkItem(BaseModel):
    title: str
    url: str


class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Student technical or placement question")
    api_key: Optional[str] = Field(default=None, description="Optional Gemini API Key")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "What is the Bias-Variance tradeoff in machine learning?",
                "api_key": None
            }
        }
    }


class ChatQueryResponse(BaseModel):
    query: str
    answer: str
    source: str = Field(..., description="'Knowledge base' or 'Web'")
    confidence: float
    matched_question: Optional[str] = None
    category: Optional[str] = None
    role: Optional[str] = None
    web_links: List[WebLinkItem] = Field(default_factory=list)


