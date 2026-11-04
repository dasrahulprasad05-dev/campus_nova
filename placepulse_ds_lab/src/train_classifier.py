"""
CampusNova AI: Multi-Model Placement Classification & Benchmark Pipeline
Module: src/train_classifier.py
Author: CampusNova AI Team
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
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
import xgboost as xgb

from feature_engineering import get_placement_preprocessor, STREAM_KEYS

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "college_placement_processed.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "placement_pipeline.joblib")
LEGACY_MODEL_PATH = os.path.join(MODELS_DIR, "placement_classifier.joblib")
METRICS_SAVE_PATH = os.path.join(MODELS_DIR, "classifier_benchmarks.json")


def train_placement_classifiers():
    print("=" * 75)
    print("PLACEPULSE AI — B.Tech Placement Classification (Leakage-Free CV Pipeline)")
    print("=" * 75)

    # 1. Load Data
    df_raw = pd.read_csv(DATA_PATH)
    print(f"Loaded Raw Records: {len(df_raw)}")

    # 2. Duplicate Audit
    dup_count = df_raw.duplicated().sum()
    print(f"Duplicate rows detected: {dup_count}")
    df = df_raw.drop_duplicates().copy()
    print(f"Deduplicated Records: {len(df)}")

    # 3. Stream Validation
    unique_streams = list(df["Stream"].unique())
    print(f"Stream categories in dataset: {unique_streams}")
    for s in unique_streams:
        if s not in STREAM_KEYS:
            print(f"⚠️ Warning: Detected unknown stream '{s}'")

    # 4. Formulate Feature Interaction
    df["CGPA_x_Intern"] = df["CGPA"] * (df["Internships"] + 1)
    feature_cols = ["CGPA", "CGPA_x_Intern", "Stream", "Internships", "HistoryOfBacklogs"]
    X = df[feature_cols]
    y = df["PlacedOrNot"].values

    # 5. Holdout Split: The test set is isolated strictly ONCE and never used for selection
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train split: {len(X_train)} | Holdout test split: {len(X_test)}")

    # 6. Model Candidates (including DummyClassifier baseline)
    candidates = {
        "Baseline (Most Frequent)": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression (L2)": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        "Random Forest (100 trees)": RandomForestClassifier(n_estimators=100, max_depth=8, criterion="entropy", random_state=42),
        "XGBoost Classifier": xgb.XGBClassifier(n_estimators=150, learning_rate=0.05, max_depth=5, eval_metric="logloss", random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }

    # 7. Model Selection via 5-Fold Stratified Cross-Validation strictly on training split
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_summary = {}
    best_cv_f1 = -1.0
    best_model_name = ""

    print("\n" + "-" * 75)
    print(f"{'Model Name':<28} | {'CV Accuracy':<12} | {'CV F1-Score':<12} | {'CV ROC-AUC':<10}")
    print("-" * 75)

    scoring = ["accuracy", "f1", "roc_auc"]

    for name, clf in candidates.items():
        # Pipeline incorporates ColumnTransformer inside CV fold
        pipe = Pipeline([
            ("pre", get_placement_preprocessor()),
            ("clf", clf)
        ])
        scores = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)
        mean_acc = float(np.mean(scores["test_accuracy"]))
        mean_f1 = float(np.mean(scores["test_f1"]))
        mean_auc = float(np.mean(scores["test_roc_auc"]))

        cv_summary[name] = {
            "cv_accuracy": round(mean_acc, 4),
            "cv_f1": round(mean_f1, 4),
            "cv_roc_auc": round(mean_auc, 4)
        }

        print(f"{name:<28} | {mean_acc:.4f}       | {mean_f1:.4f}       | {mean_auc:.4f}")

        # Pick winning model based strictly on training CV F1
        if mean_f1 > best_cv_f1:
            best_cv_f1 = mean_f1
            best_model_name = name

    print("-" * 75)
    print(f"\n[WINNER] Model Selected by 5-Fold Cross-Validation: '{best_model_name}' (CV F1: {best_cv_f1:.4f})")

    # 8. Final Evaluation on Holdout Test Split (Touched strictly ONCE)
    winning_clf = candidates[best_model_name]
    final_pipeline = Pipeline([
        ("pre", get_placement_preprocessor()),
        ("clf", winning_clf)
    ])
    final_pipeline.fit(X_train, y_train)

    y_test_pred = final_pipeline.predict(X_test)
    y_test_prob = final_pipeline.predict_proba(X_test)[:, 1] if hasattr(winning_clf, "predict_proba") else y_test_pred

    test_acc = accuracy_score(y_test, y_test_pred)
    test_prec = precision_score(y_test, y_test_pred, zero_division=0)
    test_rec = recall_score(y_test, y_test_pred, zero_division=0)
    test_f1 = f1_score(y_test, y_test_pred, zero_division=0)
    test_auc = roc_auc_score(y_test, y_test_prob)
    cm = confusion_matrix(y_test, y_test_pred).tolist()

    print("\n" + "=" * 75)
    print("FINAL UNBIASED HOLDOUT TEST SET PERFORMANCE:")
    print("=" * 75)
    print(f"Test Accuracy:  {test_acc:.4f}")
    print(f"Test Precision: {test_prec:.4f}")
    print(f"Test Recall:    {test_rec:.4f}")
    print(f"Test F1-Score:  {test_f1:.4f}")
    print(f"Test ROC-AUC:   {test_auc:.4f}")
    print("Confusion Matrix:")
    print(np.array(cm))

    # 9. Serialization: Dump whole Pipeline (No custom class required)
    print(f"\nSerializing winning Pipeline to: {MODEL_SAVE_PATH}")
    joblib.dump(final_pipeline, MODEL_SAVE_PATH)
    joblib.dump(final_pipeline, LEGACY_MODEL_PATH)

    benchmark_metadata = {
        "production_model": best_model_name,
        "best_cv_f1": round(best_cv_f1, 4),
        "test_metrics": {
            "test_accuracy": round(test_acc, 4),
            "test_precision": round(test_prec, 4),
            "test_recall": round(test_rec, 4),
            "test_f1": round(test_f1, 4),
            "roc_auc": round(test_auc, 4),
            "confusion_matrix": cm
        },
        "cv_leaderboard": cv_summary,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "deduplicated_records": len(df)
    }

    with open(METRICS_SAVE_PATH, "w") as f:
        json.dump(benchmark_metadata, f, indent=2)

    print(f"Persisted benchmark registry to: {METRICS_SAVE_PATH}")
    print("Classifier training pipeline completed successfully!\n")
    return benchmark_metadata


if __name__ == "__main__":
    train_placement_classifiers()
