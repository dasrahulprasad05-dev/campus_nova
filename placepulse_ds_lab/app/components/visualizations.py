"""
CampusNova AI: Visualization & Statistical Chart Renderers
Module: app/components/visualizations.py
Author: CampusNova AI Team
License: Approved Production Blueprint - v1.0.0
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, Any, List


def plot_confusion_matrix(cm_array: List[List[int]], title: str = "Placement Prediction Confusion Matrix"):
    """Renders a styled confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(5, 4))
    cm = np.array(cm_array)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Not Placed", "Placed"],
        yticklabels=["Not Placed", "Placed"],
        ax=ax,
        annot_kws={"size": 14, "weight": "bold"}
    )
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("True Ground Truth", fontsize=11)
    plt.tight_layout()
    return fig


def plot_model_leaderboard(leaderboard_data: Dict[str, Any]):
    """Renders a comparative bar chart for benchmarked models."""
    models = []
    accuracies = []
    f1_scores = []
    roc_aucs = []

    for name, data in leaderboard_data.items():
        models.append(name)
        accuracies.append(data.get("test_accuracy", 0.0) * 100)
        f1_scores.append(data.get("test_f1", 0.0) * 100)
        roc_aucs.append(data.get("roc_auc", 0.0) * 100)

    df = pd.DataFrame({
        "Model": models,
        "Accuracy (%)": accuracies,
        "F1-Score (%)": f1_scores,
        "ROC-AUC (%)": roc_aucs
    })

    fig, ax = plt.subplots(figsize=(9, 4.5))
    df_melt = df.melt(id_vars="Model", var_name="Metric", value_name="Score")
    sns.barplot(data=df_melt, x="Model", y="Score", hue="Metric", palette="tab10", ax=ax)
    ax.set_title("Multi-Model Placement Classifier Benchmark Comparison", fontsize=13, fontweight="bold")
    ax.set_ylabel("Score (%)")
    ax.set_ylim(80, 102)
    plt.xticks(rotation=15, ha="right")
    plt.legend(loc="lower right")
    plt.tight_layout()
    return fig


def plot_branch_placement_rates(branch_dict: Dict[str, float]):
    """Renders branch-wise campus placement success rates."""
    df = pd.DataFrame(list(branch_dict.items()), columns=["Stream", "Rate"])
    df["Percentage"] = (df["Rate"] * 100).round(1)
    df = df.sort_values(by="Percentage", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=df, x="Stream", y="Percentage", palette="viridis", ax=ax)
    ax.set_title("Campus Placement Rate by Engineering Stream", fontsize=13, fontweight="bold")
    ax.set_ylabel("Placement Success Rate (%)")
    ax.set_ylim(0, 105)
    plt.xticks(rotation=20, ha="right")
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 2),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(corr_dict: Dict[str, float]):
    """Renders Pearson correlation coefficients with the target."""
    df = pd.DataFrame(list(corr_dict.items()), columns=["Feature", "Correlation"])
    df = df.sort_values(by="Correlation", ascending=False)

    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = ["#2e7d32" if c > 0 else "#c62828" for c in df["Correlation"]]
    sns.barplot(data=df, x="Correlation", y="Feature", palette=colors, ax=ax)
    ax.set_title("Feature Correlations with Placement Probability", fontsize=12, fontweight="bold")
    ax.set_xlim(-0.6, 0.8)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7)
    for p in ax.patches:
        val = p.get_width()
        offset = 0.02 if val >= 0 else -0.08
        ax.annotate(f"{val:.3f}", (val + offset, p.get_y() + p.get_height() / 2.),
                    va='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    return fig

