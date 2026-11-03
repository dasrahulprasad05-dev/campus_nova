"""
PlacePulse AI: Resume Domain Classification & NLP Model Pipeline
Module: src/train_nlp.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report

from feature_engineering import clean_resume_text, create_resume_vectorizer

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "resumes_processed.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "resume_classifier.joblib")
VECTORIZER_SAVE_PATH = os.path.join(MODELS_DIR, "resume_tfidf.joblib")
LABEL_ENCODER_PATH = os.path.join(MODELS_DIR, "resume_label_encoder.joblib")
METRICS_SAVE_PATH = os.path.join(MODELS_DIR, "nlp_benchmarks.json")


def train_resume_nlp_models():
    print("=" * 75)
    print("PLACEPULSE AI — Resume Domain Classification (25+ Categories & CV Pipeline)")
    print("=" * 75)

    # 1. Load Data
    df_raw = pd.read_csv(DATA_PATH)
    print(f"Loaded Raw Resumes: {len(df_raw)}")

    # 2. Duplicate Audit
    dup_count = df_raw.duplicated(subset=["Resume"]).sum()
    print(f"Duplicate resume texts detected: {dup_count}")
    df = df_raw.drop_duplicates(subset=["Resume"]).copy()
    print(f"Deduplicated Resumes: {len(df)} across {df['Category'].nunique()} roles")

    # 3. Label Encoding
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["Category"].values)
    classes = list(label_encoder.classes_)

    # 4. Clean Resume Text (Safely preserving tech tokens e.g. cpp, cicd, scikitlearn)
    cleaned_texts = [clean_resume_text(t) for t in df["Resume"].values]

    # 5. Train-Test Split (80/20 Stratified)
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        cleaned_texts, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training resumes: {len(X_train_raw)} | Testing resumes: {len(X_test_raw)}")

    # 6. Model Pipeline Candidates (TF-IDF vectorizer + Classifier)
    candidates = {
        "Linear SVC": LinearSVC(C=1.0, random_state=42, max_iter=2000),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Logistic Regression (Multi)": LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_summary = {}
    best_cv_f1 = -1.0
    best_model_name = ""

    print("\n" + "-" * 75)
    print(f"{'NLP Pipeline Candidate':<32} | {'CV Accuracy':<12} | {'CV Weighted F1':<12}")
    print("-" * 75)

    scoring = ["accuracy", "f1_weighted"]

    for name, clf in candidates.items():
        pipe = Pipeline([
            ("tfidf", create_resume_vectorizer(max_features=1500)),
            ("clf", clf)
        ])
        scores = cross_validate(pipe, X_train_raw, y_train, cv=cv, scoring=scoring)
        mean_acc = float(np.mean(scores["test_accuracy"]))
        mean_f1 = float(np.mean(scores["test_f1_weighted"]))

        cv_summary[name] = {
            "cv_accuracy": round(mean_acc, 4),
            "cv_weighted_f1": round(mean_f1, 4)
        }
        print(f"{name:<32} | {mean_acc:.4f}       | {mean_f1:.4f}")

        if mean_f1 > best_cv_f1:
            best_cv_f1 = mean_f1
            best_model_name = name

    print("-" * 75)
    print(f"\n[WINNER] Selected NLP Classifier via 5-Fold CV: '{best_model_name}' (CV F1: {best_cv_f1:.4f})")

    # 7. Final Training & Single Holdout Evaluation
    winning_clf = candidates[best_model_name]
    final_vectorizer = create_resume_vectorizer(max_features=1500)
    X_train_vec = final_vectorizer.fit_transform(X_train_raw)
    X_test_vec = final_vectorizer.transform(X_test_raw)

    winning_clf.fit(X_train_vec, y_train)
    y_test_pred = winning_clf.predict(X_test_vec)

    test_acc = accuracy_score(y_test, y_test_pred)
    test_weighted_f1 = f1_score(y_test, y_test_pred, average="weighted", zero_division=0)

    print("\n" + "=" * 75)
    print("FINAL UNBIASED HOLDOUT TEST SET PERFORMANCE:")
    print("=" * 75)
    print(f"Test Accuracy:    {test_acc:.4f}")
    print(f"Test Weighted F1: {test_weighted_f1:.4f}")

    # 8. Serialization
    print(f"\nSaving winning model to: {MODEL_SAVE_PATH}")
    joblib.dump(winning_clf, MODEL_SAVE_PATH)
    joblib.dump(final_vectorizer, VECTORIZER_SAVE_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)

    metadata = {
        "production_model": best_model_name,
        "best_cv_f1": round(best_cv_f1, 4),
        "test_metrics": {
            "test_accuracy": round(test_acc, 4),
            "test_weighted_f1": round(test_weighted_f1, 4)
        },
        "cv_leaderboard": cv_summary,
        "target_classes": classes,
        "vocabulary_size": int(X_train_vec.shape[1]),
        "total_records": len(df)
    }

    with open(METRICS_SAVE_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Persisted NLP metrics to: {METRICS_SAVE_PATH}")
    print("Resume NLP pipeline training complete!\n")
    return metadata


if __name__ == "__main__":
    train_resume_nlp_models()
