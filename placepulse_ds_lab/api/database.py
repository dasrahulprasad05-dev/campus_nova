"""
CampusNova AI: Database Connection & Schema Management
Module: api/database.py
Author: CampusNova AI Team
License: Approved Production Blueprint - v1.0.0
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "placepulse.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Initializes the SQLite relational database with the 3 required production tables:
    1. placement_predictions
    2. resume_evaluations
    3. model_benchmark_registry
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS placement_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name VARCHAR(100),
        stream VARCHAR(50) NOT NULL,
        cgpa REAL NOT NULL,
        internships INTEGER NOT NULL DEFAULT 0,
        history_of_backlogs BOOLEAN NOT NULL DEFAULT 0,
        aptitude_score REAL,
        predicted_placement BOOLEAN NOT NULL,
        placement_probability REAL NOT NULL,
        predicted_ctc_lpa REAL,
        model_version VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_name VARCHAR(100),
        raw_resume_snippet TEXT NOT NULL,
        predicted_category VARCHAR(100) NOT NULL,
        confidence_score REAL NOT NULL,
        matched_skills TEXT,
        missing_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_benchmark_registry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name VARCHAR(100) NOT NULL,
        task_type VARCHAR(50) NOT NULL,
        accuracy REAL,
        f1_score REAL,
        roc_auc REAL,
        mae REAL,
        is_production_active BOOLEAN DEFAULT 0,
        trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def log_placement_prediction(
    stream: str,
    cgpa: float,
    internships: int,
    backlogs: int,
    predicted_placement: bool,
    placement_probability: float,
    student_name: Optional[str] = None,
    aptitude_score: Optional[float] = None,
    predicted_ctc_lpa: Optional[float] = None,
    model_version: str = "v1.0.0"
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO placement_predictions (
            student_name, stream, cgpa, internships, history_of_backlogs,
            aptitude_score, predicted_placement, placement_probability,
            predicted_ctc_lpa, model_version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name, stream, cgpa, internships, backlogs,
        aptitude_score, int(predicted_placement), placement_probability,
        predicted_ctc_lpa, model_version
    ))
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prediction_id


def log_resume_evaluation(
    raw_resume_snippet: str,
    predicted_category: str,
    confidence_score: float,
    matched_skills: List[str],
    missing_skills: List[str],
    candidate_name: Optional[str] = None
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resume_evaluations (
            candidate_name, raw_resume_snippet, predicted_category,
            confidence_score, matched_skills, missing_skills
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        raw_resume_snippet[:500],
        predicted_category,
        confidence_score,
        json.dumps(matched_skills),
        json.dumps(missing_skills)
    ))
    evaluation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return evaluation_id


def sync_benchmark_registry(classifier_benchmarks: Dict[str, Any], regressor_benchmarks: Dict[str, Any], nlp_benchmarks: Dict[str, Any]):
    """Populates model_benchmark_registry from current training results."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear old entries to keep active benchmark state synchronized
    cursor.execute("DELETE FROM model_benchmark_registry")

    # Classification models
    clf_active = classifier_benchmarks.get("production_model", "")
    for name, metrics in classifier_benchmarks.get("leaderboard", {}).items():
        cursor.execute("""
            INSERT INTO model_benchmark_registry (
                model_name, task_type, accuracy, f1_score, roc_auc, mae, is_production_active
            ) VALUES (?, 'classification', ?, ?, ?, NULL, ?)
        """, (
            name,
            metrics.get("test_accuracy"),
            metrics.get("test_f1"),
            metrics.get("roc_auc"),
            1 if name == clf_active else 0
        ))

    # Regression models
    reg_active = regressor_benchmarks.get("production_model", "")
    for name, metrics in regressor_benchmarks.get("leaderboard", {}).items():
        cursor.execute("""
            INSERT INTO model_benchmark_registry (
                model_name, task_type, accuracy, f1_score, roc_auc, mae, is_production_active
            ) VALUES (?, 'regression', NULL, NULL, NULL, ?, ?)
        """, (
            name,
            metrics.get("test_mae"),
            1 if name == reg_active else 0
        ))

    # NLP models
    nlp_active = nlp_benchmarks.get("production_model", "")
    for name, metrics in nlp_benchmarks.get("leaderboard", {}).items():
        cursor.execute("""
            INSERT INTO model_benchmark_registry (
                model_name, task_type, accuracy, f1_score, roc_auc, mae, is_production_active
            ) VALUES (?, 'nlp', ?, ?, NULL, NULL, ?)
        """, (
            name,
            metrics.get("test_accuracy"),
            metrics.get("weighted_f1"),
            1 if name == nlp_active else 0
        ))

    conn.commit()
    conn.close()


def get_recent_predictions(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM placement_predictions ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully at:", DB_PATH)

