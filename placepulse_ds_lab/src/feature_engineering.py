"""
PlacePulse AI: Feature Engineering Pipeline & Text Preprocessor
Module: src/feature_engineering.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0
"""

import re
import string
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any, Optional
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

# Canonical Stream Mapping & Validation List
STREAM_KEYS = [
    "Computer Science",
    "Information Technology",
    "Electronics And Communication",
    "Mechanical",
    "Electrical",
    "Civil"
]

# Comprehensive Skill Taxonomy covering ALL 25 categories in UpdatedResumeDataSet
TECH_SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Data Science": [
        "python", "machine learning", "deep learning", "pandas", "numpy",
        "scikit-learn", "nlp", "sql", "statistics", "tensorflow", "pytorch",
        "data visualization", "tableau", "power bi", "feature engineering",
        "data analysis", "random forest", "xgboost", "big data"
    ],
    "Java Developer": [
        "java", "spring boot", "microservices", "hibernate", "rest api",
        "maven", "junit", "multithreading", "postgresql", "mysql",
        "kafka", "design patterns", "docker", "jvm", "spring cloud", "core java", "git"
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "ci/cd", "aws", "terraform", "jenkins",
        "linux", "ansible", "gitlab ci", "prometheus", "grafana", "bash",
        "helm", "cloudwatch", "git", "infrastructure as code"
    ],
    "Web Designing": [
        "html5", "css3", "javascript", "react", "next.js", "tailwind css",
        "ui/ux", "responsive design", "figma", "redux", "typescript",
        "node.js", "bootstrap", "front-end"
    ],
    "Python Developer": [
        "python", "django", "fastapi", "flask", "celery", "redis",
        "sqlalchemy", "rest api", "postgresql", "oop", "pytest", "asyncio",
        "git", "docker", "linux"
    ],
    "Network Security Engineer": [
        "firewall", "tcp/ip", "wireshark", "penetration testing", "cisco",
        "network protocols", "siem", "vpn", "ethical hacking", "intrusion detection",
        "vulnerability assessment", "cybersecurity", "cryptography"
    ],
    "Mechanical Engineer": [
        "solidworks", "autocad", "thermodynamics", "fluid mechanics",
        "fea analysis", "ansys", "manufacturing processes", "gd&t",
        "machine design", "cad/cam", "cnc"
    ],
    "Civil Engineer": [
        "autocad", "structural analysis", "staad pro", "revit",
        "concrete technology", "surveying", "geotechnical", "estimation",
        "site supervision", "bim"
    ],
    "Electrical Engineering": [
        "circuit design", "power systems", "matlab", "plc scada",
        "microcontrollers", "embedded systems", "electrical machines",
        "vlsi", "power electronics", "pcb"
    ],
    "Database": [
        "sql", "mysql", "postgresql", "database administration",
        "query optimization", "indexing", "stored procedures", "etl",
        "nosql", "mongodb", "data modeling", "oracle"
    ],
    "Blockchain": [
        "solidity", "smart contracts", "ethereum", "web3.js", "hyperledger",
        "cryptography", "truffle", "hardhat", "consensus algorithms", "dapps"
    ],
    "Automation Testing": [
        "selenium", "testng", "java", "python", "cucumber bdd", "appium",
        "jenkins", "api testing", "postman", "regression testing", "jira"
    ],
    "Business Analyst": [
        "requirements gathering", "brd", "user stories", "agile", "scrum",
        "tableau", "power bi", "excel", "data modeling", "stakeholder management"
    ],
    "Operations Manager": [
        "supply chain", "process optimization", "six sigma", "operations strategy",
        "vendor management", "budgeting", "lean manufacturing", "kpi tracking"
    ],
    "DotNet Developer": [
        "c#", ".net core", "asp.net mvc", "entity framework",
        "sql server", "web api", "linq", "azure", "microservices"
    ],
    "SAP Developer": [
        "sap abap", "sap hana", "bapi", "idoc", "fiori", "rfc",
        "alv reports", "smartforms", "debugging", "data dictionary"
    ],
    "ETL Developer": [
        "informatica", "talend", "data warehousing", "data pipelines", "sql",
        "ssis", "dimensional modeling", "data quality", "airflow"
    ],
    "Hadoop": [
        "hdfs", "mapreduce", "hive", "pig", "apache spark", "sqoop",
        "kafka", "zookeeper", "cloudera", "big data analytics"
    ],
    "Testing": [
        "manual testing", "test cases", "bug reporting", "jira",
        "black box testing", "regression", "stlc", "sdlc", "functional testing"
    ],
    "HR": [
        "recruitment", "talent acquisition", "employee relations", "onboarding",
        "payroll", "performance management", "hr policies", "hrms"
    ],
    "Advocate": [
        "legal research", "corporate law", "contract drafting", "litigation",
        "arbitration", "intellectual property", "legal compliance", "due diligence"
    ],
    "Arts": [
        "graphic design", "illustration", "creative direction", "typography",
        "adobe photoshop", "illustrator", "visual storytelling", "animation"
    ],
    "Sales": [
        "b2b sales", "client acquisition", "lead generation", "sales pipeline",
        "negotiation", "crm", "sales forecasting", "account management"
    ],
    "Health and fitness": [
        "personal training", "nutrition planning", "kinesiology", "exercise physiology",
        "strength conditioning", "wellness coaching", "rehabilitation"
    ],
    "PMO": [
        "project management", "pmp", "milestone tracking", "risk management",
        "resource allocation", "governance", "status reporting", "prince2"
    ]
}


def normalize_token_stream(text: str) -> str:
    """
    Normalizes text for NLP vectorization while safely preserving key tech terms.
    e.g., 'c++', 'c#', '.net', 'ci/cd', 'node.js', 'scikit-learn'.
    """
    if not isinstance(text, str):
        return ""

    # Preserve special symbols before general punctuation stripping
    text = re.sub(r'\bc\+\+\b', ' cpp ', text, flags=re.IGNORECASE)
    text = re.sub(r'\bc#\b', ' csharp ', text, flags=re.IGNORECASE)
    text = re.sub(r'\.net\b', ' dotnet ', text, flags=re.IGNORECASE)
    text = re.sub(r'\bnode\.js\b', ' nodejs ', text, flags=re.IGNORECASE)
    text = re.sub(r'\bnext\.js\b', ' nextjs ', text, flags=re.IGNORECASE)
    text = re.sub(r'\bci/cd\b', ' cicd ', text, flags=re.IGNORECASE)
    text = re.sub(r'\bscikit-learn\b', ' scikitlearn ', text, flags=re.IGNORECASE)

    # Strip URLs
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'www\.\S+\s*', ' ', text)
    # Strip emails
    text = re.sub(r'\S+@\S+', ' ', text)
    # Strip mentions & hashtags
    text = re.sub(r'[@#]\S+', ' ', text)
    # Strip punctuation
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    # Strip non-ASCII
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def clean_resume_text(text: str) -> str:
    """Standardized resume text cleaning."""
    return normalize_token_stream(text)


def normalize_skill_name(skill: str) -> str:
    """Normalizes skill keywords in the exact same manner as resume text."""
    return normalize_token_stream(skill)


def analyze_skill_gaps(resume_text: str, target_role: str) -> Dict[str, Any]:
    """
    Deterministic Skill-Gap extraction against target job domain.
    If the requested role is not in TECH_SKILL_TAXONOMY, it reports has_taxonomy=False
    rather than silently defaulting to a wrong role.
    """
    cleaned_resume = normalize_token_stream(resume_text)

    # Check taxonomy availability
    if target_role not in TECH_SKILL_TAXONOMY:
        return {
            "target_role": target_role,
            "has_taxonomy": False,
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "total_skills_evaluated": 0,
            "message": f"No curated skill taxonomy available for role: '{target_role}'."
        }

    raw_skills = TECH_SKILL_TAXONOMY[target_role]
    matched = []
    missing = []

    for s in raw_skills:
        norm_s = normalize_skill_name(s)
        # Search word boundaries in normalized resume
        pattern = r'\b' + re.escape(norm_s) + r'\b'
        if re.search(pattern, cleaned_resume):
            matched.append(s.title())
        else:
            missing.append(s.title())

    total = len(raw_skills)
    match_pct = round((len(matched) / max(total, 1)) * 100, 1)

    return {
        "target_role": target_role,
        "has_taxonomy": True,
        "match_percentage": match_pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "total_skills_evaluated": total,
        "message": f"Evaluated against {total} curated competencies for {target_role}."
    }


def get_placement_preprocessor() -> ColumnTransformer:
    """
    Constructs an explicit Scikit-Learn ColumnTransformer for placement classification:
    - Scales continuous features: ['CGPA', 'CGPA_x_Intern']
    - One-hot encodes categorical stream: ['Stream']
    - Passes through binary & integer counts: ['Internships', 'HistoryOfBacklogs']
    Fit strictly on training folds to prevent any data leakage.
    """
    return ColumnTransformer([
        ("num", StandardScaler(), ["CGPA", "CGPA_x_Intern"]),
        ("cat", OneHotEncoder(categories=[STREAM_KEYS], handle_unknown="ignore", sparse_output=False), ["Stream"]),
        ("keep", "passthrough", ["Internships", "HistoryOfBacklogs"])
    ])


def get_salary_preprocessor() -> ColumnTransformer:
    """
    Constructs an explicit ColumnTransformer for CTC salary regression:
    - Scales: ['degree_p', 'etest_p']
    - Passes: ['workex_binary']
    Eliminates dead columns and prevents test-set data leakage.
    """
    return ColumnTransformer([
        ("num", StandardScaler(), ["degree_p", "etest_p"]),
        ("keep", "passthrough", ["workex_binary"])
    ])


def create_resume_vectorizer(max_features: int = 1500) -> TfidfVectorizer:
    """Sublinear TF-IDF vectorizer matching production specification."""
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words="english"
    )
