"""
PlacePulse AI: CTC / Salary Package Regression Pipeline
Module: src/train_regressor.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0

NOTE ON DATASET DOMAIN INTEGRITY:
The Ben Roshan Campus Recruitment benchmark dataset is based on institutional recruitment
with MBA and undergraduate degree records (degree_p, etest_p, workex, salary).
In PlacePulse AI, this dataset serves as an empirical compensation benchmark for campus hiring
and aptitude evaluation. It is explicitly labeled as general campus recruitment compensation,
rather than exclusively B.Tech engineering salaries.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any

from sklearn.model_selection import train_test_split, KFold, RepeatedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from feature_engineering import get_salary_preprocessor

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "salary_placed_processed.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "salary_pipeline.joblib")
LEGACY_MODEL_PATH = os.path.join(MODELS_DIR, "salary_regressor.joblib")
METRICS_SAVE_PATH = os.path.join(MODELS_DIR, "regressor_benchmarks.json")


def train_salary_regressors():
    print("=" * 75)
    print("PLACEPULSE AI — Campus CTC Salary Regression (Leakage-Free Repeated CV)")
    print("=" * 75)

    # 1. Load Data
    df_raw = pd.read_csv(DATA_PATH)
    print(f"Total Placed Offers Available: {len(df_raw)}")
    print(f"Salary Currency & Unit: INR in Lakhs Per Annum (LPA)")
    print(f"Salary Range: {df_raw['salary_lpa'].min():.2f} LPA to {df_raw['salary_lpa'].max():.2f} LPA (Mean: {df_raw['salary_lpa'].mean():.2f} LPA)")

    # 2. Check Duplicates
    dup_count = df_raw.duplicated().sum()
    print(f"Duplicate placed rows: {dup_count}")
    df = df_raw.drop_duplicates().copy()

    # 3. Clean Features (No dead columns)
    feature_cols = ["degree_p", "etest_p", "workex_binary"]
    X = df[feature_cols]
    y = df["salary_lpa"].values

    # 4. Holdout Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"Train split: {len(X_train)} samples | Test holdout: {len(X_test)} samples")

    # 5. Model Candidates with Dummy Baseline
    candidates = {
        "Baseline (Predict Mean)": DummyRegressor(strategy="mean"),
        "Baseline (Predict Median)": DummyRegressor(strategy="median"),
        "Ridge Regression (alpha=1.0)": Ridge(alpha=1.0, random_state=42),
        "Linear Regression (OLS)": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
    }

    # 6. Model Selection using Repeated K-Fold CV (5 folds x 5 repeats) on training split
    rkf = RepeatedKFold(n_splits=5, n_repeats=5, random_state=42)
    cv_summary = {}
    best_cv_mae = float("inf")
    best_model_name = ""

    print("\n" + "-" * 75)
    print(f"{'Regressor Model':<32} | {'Repeated CV MAE':<16} | {'CV R2 Score':<12}")
    print("-" * 75)

    scoring = ["neg_mean_absolute_error", "r2"]

    for name, reg in candidates.items():
        pipe = Pipeline([
            ("pre", get_salary_preprocessor()),
            ("reg", reg)
        ])
        scores = cross_validate(pipe, X_train, y_train, cv=rkf, scoring=scoring)
        mean_mae = -float(np.mean(scores["test_neg_mean_absolute_error"]))
        mean_r2 = float(np.mean(scores["test_r2"]))

        cv_summary[name] = {
            "cv_mae": round(mean_mae, 4),
            "cv_r2": round(mean_r2, 4)
        }

        print(f"{name:<32} | {mean_mae:.4f} LPA         | {mean_r2:.4f}")

        # Pick best model strictly on training CV MAE (excluding baseline)
        if "Baseline" not in name and mean_mae < best_cv_mae:
            best_cv_mae = mean_mae
            best_model_name = name

    print("-" * 75)
    print(f"\n[WINNER] Model Selected by Repeated CV: '{best_model_name}' (CV MAE: {best_cv_mae:.4f} LPA)")

    # 7. Final Holdout Evaluation (Touched strictly ONCE)
    winning_reg = candidates[best_model_name]
    final_pipeline = Pipeline([
        ("pre", get_salary_preprocessor()),
        ("reg", winning_reg)
    ])
    final_pipeline.fit(X_train, y_train)

    y_test_pred = final_pipeline.predict(X_test)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_r2 = r2_score(y_test, y_test_pred)

    # Baseline performance on test set
    dummy_pred = np.full_like(y_test, np.mean(y_train))
    dummy_mae = mean_absolute_error(y_test, dummy_pred)

    print("\n" + "=" * 75)
    print("FINAL UNBIASED HOLDOUT TEST SET PERFORMANCE:")
    print("=" * 75)
    print(f"Test MAE:       {test_mae:.4f} LPA (vs Mean Baseline MAE: {dummy_mae:.4f} LPA)")
    print(f"Test RMSE:      {test_rmse:.4f} LPA")
    print(f"Test R2 Score:  {test_r2:.4f}")
    print(f"MAE Reduction:  {((dummy_mae - test_mae) / dummy_mae) * 100:.1f}% over baseline")

    # 8. Serialization: Export Pipeline
    print(f"\nSerializing winning Pipeline to: {MODEL_SAVE_PATH}")
    joblib.dump(final_pipeline, MODEL_SAVE_PATH)
    joblib.dump(final_pipeline, LEGACY_MODEL_PATH)

    metadata = {
        "production_model": best_model_name,
        "best_cv_mae_lpa": round(best_cv_mae, 4),
        "test_metrics": {
            "test_mae_lpa": round(test_mae, 4),
            "test_rmse_lpa": round(test_rmse, 4),
            "test_r2": round(test_r2, 4),
            "dummy_baseline_mae": round(dummy_mae, 4)
        },
        "repeated_cv_leaderboard": cv_summary,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "dataset_disclaimer": "Benchmark based on campus management & tech recruitment records (Ben Roshan dataset)."
    }

    with open(METRICS_SAVE_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Persisted regression metrics to: {METRICS_SAVE_PATH}")
    print("Salary regression training complete!\n")
    return metadata


if __name__ == "__main__":
    train_salary_regressors()
