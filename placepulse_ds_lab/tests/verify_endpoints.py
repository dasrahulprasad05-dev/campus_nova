"""
Verification script for all PlacePulse AI endpoints
"""
import sys
import os
import asyncio

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, os.path.join(PROJECT_DIR, "src"))
sys.path.insert(0, os.path.join(PROJECT_DIR, "api"))

from main import (
    health_check, predict_placement, predict_salary, screen_resume,
    explain_at_risk, get_eda_metrics, get_interview_questions,
    PlacementPredictionRequest, SalaryPredictionRequest, ResumeScreenRequest,
    AtRiskExplainerRequest, InterviewQuestionRequest
)


async def main():
    print("Testing health endpoint...")
    h = await health_check()
    print(f"Health Status: {h.status} | Models Loaded: {h.models_loaded}")
    assert h.status == "ok"
    assert h.models_loaded is True

    print("\nTesting placement prediction (High Potential)...")
    p1 = await predict_placement(PlacementPredictionRequest(
        stream="Computer Science", cgpa=8.5, internships=2, backlogs=0
    ))
    print(f"Verdict: {p1.verdict} | Probability: {p1.probability}% | ID: {p1.prediction_id}")
    assert p1.placed is True

    print("\nTesting placement prediction (At-Risk)...")
    p2 = await predict_placement(PlacementPredictionRequest(
        stream="Civil", cgpa=5.8, internships=0, backlogs=1
    ))
    print(f"Verdict: {p2.verdict} | Probability: {p2.probability}%")
    assert p2.placed is False

    print("\nTesting CTC salary prediction...")
    s = await predict_salary(SalaryPredictionRequest(
        cgpa=8.2, aptitude_score=85.0, internships=1, stream="Computer Science"
    ))
    print(f"Predicted CTC: {s.predicted_ctc_lpa} LPA | Interval: {s.range}")
    assert s.predicted_ctc_lpa > 2.5

    print("\nTesting Resume Screening NLP...")
    r = await screen_resume(ResumeScreenRequest(
        resume_text="Experienced Python Developer specializing in FastAPI, Django, Docker, PostgreSQL, Microservices and AWS.",
        target_role="Python Developer"
    ))
    print(f"Predicted Role: {r.predicted_role} | Matched: {r.matched_skills[:4]} | Missing: {r.missing_skills[:3]}")
    assert "Python" in r.predicted_role or "Data" in r.predicted_role or "Developer" in r.predicted_role

    print("\nTesting At-Risk Explainer...")
    e = await explain_at_risk(AtRiskExplainerRequest(
        stream="Mechanical", cgpa=6.1, internships=0, backlogs=1
    ))
    print(f"Is At Risk: {e.is_at_risk} | Risk Score: {e.risk_score} | Negative Factors: {len(e.top_negative_factors)}")
    assert e.is_at_risk is True

    print("\nTesting EDA Metrics...")
    eda = await get_eda_metrics()
    print(f"Total analyzed records: {eda.total_records_analyzed}")
    print(f"Sample Branch Placement Rates: {list(eda.branch_placement_rates.items())[:3]}")

    print("\nTesting Interview QA Recommendation...")
    qa = await get_interview_questions(InterviewQuestionRequest(
        role="Data Science", stream="Computer Science"
    ))
    print(f"Questions Returned: {qa.total_found}")
    print(f"Sample Question: {qa.questions[0].question}")

    print("\n>>> ALL PLACEPULSE AI ENDPOINTS PASSED VERIFICATION WITH 100% SUCCESS! <<<")


if __name__ == "__main__":
    asyncio.run(main())

