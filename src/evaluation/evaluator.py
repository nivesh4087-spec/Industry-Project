"""
Model Evaluator Module
======================
Comprehensive model evaluation with metrics, plots, and ablation studies.

Generates:
- Precision, Recall, F1, PR-AUC, ROC-AUC
- Confusion matrices
- ROC curves
- Precision-Recall curves
- Calibration curves
- Model comparison tables and charts
- Ablation study results

All plots are saved to reports/figures/ in publication-quality resolution.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    brier_score_loss,
)
from sklearn.calibration import calibration_curve

logger = logging.getLogger(__name__)

# Plot style
plt.style.use("seaborn-v0_8-darkgrid")
COLORS = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
FIG_DPI = 150


def evaluate_model_on_test(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str = "Model",
) -> Dict[str, Any]:
    """Evaluate a single model on the test set.

    Args:
        model: Trained model.
        X_test: Test features.
        y_test: Test labels.
        model_name: Name for logging.

    Returns:
        Evaluation metrics dictionary.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model": model_name,
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
        "pr_auc": round(float(average_precision_score(y_test, y_prob)), 4),
        "brier_score": round(float(brier_score_loss(y_test, y_prob)), 4),
        "classification_report": classification_report(
            y_test, y_pred, target_names=["No Failure", "Failure"], output_dict=True
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    logger.info(
        "%s Test — F1: %.4f, Precision: %.4f, Recall: %.4f, PR-AUC: %.4f",
        model_name, metrics["f1"], metrics["precision"], metrics["recall"],
        metrics["pr_auc"]
    )

    return metrics


def evaluate_all_models(
    models: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> List[Dict[str, Any]]:
    """Evaluate all models on the test set.

    Args:
        models: Dictionary mapping model names to fitted models.
        X_test: Test features.
        y_test: Test labels.

    Returns:
        List of evaluation result dictionaries.
    """
    results = []
    for name, model in models.items():
        metrics = evaluate_model_on_test(model, X_test, y_test, name)
        results.append(metrics)

    return results


# ============================================================================
# Visualization Functions
# ============================================================================

def plot_confusion_matrices(
    models: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    save_dir: Path = None,
) -> plt.Figure:
    """Plot confusion matrices for all models side by side.

    Args:
        models: Dictionary of model name → fitted model.
        X_test: Test features.
        y_test: Test labels.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    n_models = len(models)
    fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 4))
    if n_models == 1:
        axes = [axes]

    for ax, (name, model) in zip(axes, models.items()):
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)

        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues", ax=ax,
            xticklabels=["No Failure", "Failure"],
            yticklabels=["No Failure", "Failure"],
            cbar=False,
        )
        ax.set_title(name, fontsize=12, fontweight="bold")
        ax.set_ylabel("Actual")
        ax.set_xlabel("Predicted")

    fig.suptitle("Confusion Matrices — Test Set", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "confusion_matrices.png", dpi=FIG_DPI, bbox_inches="tight")
        logger.info("Saved confusion matrices plot.")

    return fig


def plot_roc_curves(
    models: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    save_dir: Path = None,
) -> plt.Figure:
    """Plot ROC curves for all models.

    Args:
        models: Dictionary of model name → fitted model.
        X_test: Test features.
        y_test: Test labels.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    for i, (name, model) in enumerate(models.items()):
        y_prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc_score = auc(fpr, tpr)

        ax.plot(fpr, tpr, color=COLORS[i % len(COLORS)],
                label=f"{name} (AUC = {auc_score:.4f})", linewidth=2)

    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Random Classifier")
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curves — Model Comparison", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "roc_curves.png", dpi=FIG_DPI, bbox_inches="tight")
        logger.info("Saved ROC curves plot.")

    return fig


def plot_precision_recall_curves(
    models: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    save_dir: Path = None,
) -> plt.Figure:
    """Plot Precision-Recall curves for all models.

    PR curves are more informative than ROC curves for imbalanced datasets
    because they focus on the minority class performance.

    Args:
        models: Dictionary of model name → fitted model.
        X_test: Test features.
        y_test: Test labels.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    baseline = y_test.mean()

    for i, (name, model) in enumerate(models.items()):
        y_prob = model.predict_proba(X_test)[:, 1]
        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        ap = average_precision_score(y_test, y_prob)

        ax.plot(recall, precision, color=COLORS[i % len(COLORS)],
                label=f"{name} (AP = {ap:.4f})", linewidth=2)

    ax.axhline(y=baseline, color="k", linestyle="--", alpha=0.5,
               label=f"Baseline (prevalence = {baseline:.3f})")
    ax.set_xlabel("Recall", fontsize=12)
    ax.set_ylabel("Precision", fontsize=12)
    ax.set_title("Precision-Recall Curves — Model Comparison",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "precision_recall_curves.png", dpi=FIG_DPI, bbox_inches="tight")
        logger.info("Saved Precision-Recall curves plot.")

    return fig


def plot_calibration_curves(
    models: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    save_dir: Path = None,
) -> plt.Figure:
    """Plot calibration curves for all models.

    Well-calibrated models have curves close to the diagonal.

    Args:
        models: Dictionary of model name → fitted model.
        X_test: Test features.
        y_test: Test labels.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    for i, (name, model) in enumerate(models.items()):
        y_prob = model.predict_proba(X_test)[:, 1]
        fraction_pos, mean_predicted = calibration_curve(
            y_test, y_prob, n_bins=10, strategy="uniform"
        )

        brier = brier_score_loss(y_test, y_prob)
        ax.plot(mean_predicted, fraction_pos, "s-", color=COLORS[i % len(COLORS)],
                label=f"{name} (Brier = {brier:.4f})", linewidth=2, markersize=6)

    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Perfectly Calibrated")
    ax.set_xlabel("Mean Predicted Probability", fontsize=12)
    ax.set_ylabel("Fraction of Positives", fontsize=12)
    ax.set_title("Calibration Curves — Model Comparison",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "calibration_curves.png", dpi=FIG_DPI, bbox_inches="tight")
        logger.info("Saved calibration curves plot.")

    return fig


def plot_model_comparison_bars(
    results: List[Dict[str, Any]],
    save_dir: Path = None,
) -> plt.Figure:
    """Plot bar chart comparing all models across metrics.

    Args:
        results: List of evaluation result dictionaries.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    metrics = ["precision", "recall", "f1", "roc_auc", "pr_auc"]
    labels = ["Precision", "Recall", "F1-Score", "ROC-AUC", "PR-AUC"]
    model_names = [r["model"] for r in results]

    x = np.arange(len(labels))
    width = 0.8 / len(model_names)

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, result in enumerate(results):
        values = [result[m] for m in metrics]
        offset = (i - len(model_names) / 2 + 0.5) * width
        bars = ax.bar(x + offset, values, width, label=result["model"],
                      color=COLORS[i % len(COLORS)], alpha=0.85)
        # Add value labels on bars
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.01,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=7, fontweight="bold")

    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Model Performance Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(loc="lower right", fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "model_comparison_bars.png", dpi=FIG_DPI, bbox_inches="tight")
        logger.info("Saved model comparison bar chart.")

    return fig


def plot_class_distribution(
    y: pd.Series,
    title: str = "Class Distribution",
    save_dir: Path = None,
) -> plt.Figure:
    """Plot class distribution bar chart.

    Args:
        y: Target series.
        title: Plot title.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = y.value_counts()

    bars = ax.bar(
        ["No Failure (0)", "Failure (1)"],
        [counts.get(0, 0), counts.get(1, 0)],
        color=["#2ecc71", "#e74c3c"],
        alpha=0.85,
        edgecolor="white",
        linewidth=1.5,
    )

    for bar, count in zip(bars, [counts.get(0, 0), counts.get(1, 0)]):
        pct = count / len(y) * 100
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 20,
                f"{count}\n({pct:.1f}%)", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("Count", fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "class_distribution.png", dpi=FIG_DPI, bbox_inches="tight")

    return fig


def plot_feature_distributions(
    df: pd.DataFrame,
    target_col: str = "machine_failure",
    save_dir: Path = None,
) -> plt.Figure:
    """Plot feature distributions split by failure status.

    Args:
        df: DataFrame with features and target.
        target_col: Target column name.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    feature_cols = [c for c in df.columns
                    if c != target_col and df[c].dtype in [np.float64, np.int64, float, int]]
    n_features = min(len(feature_cols), 12)
    feature_cols = feature_cols[:n_features]

    ncols = 3
    nrows = (n_features + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, col in enumerate(feature_cols):
        if i >= len(axes):
            break
        ax = axes[i]
        for label, color in [(0, "#2ecc71"), (1, "#e74c3c")]:
            subset = df[df[target_col] == label][col].dropna()
            ax.hist(subset, bins=30, alpha=0.6, color=color,
                    label=f"{'No Fail' if label == 0 else 'Fail'}", density=True)
        ax.set_title(col, fontsize=10, fontweight="bold")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    # Hide unused axes
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Feature Distributions by Failure Status",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "feature_distributions.png", dpi=FIG_DPI, bbox_inches="tight")

    return fig


def plot_correlation_heatmap(
    df: pd.DataFrame,
    save_dir: Path = None,
) -> plt.Figure:
    """Plot correlation heatmap.

    Args:
        df: DataFrame with numerical features.
        save_dir: Directory to save figure.

    Returns:
        Matplotlib Figure.
    """
    numerical_df = df.select_dtypes(include=[np.number])
    corr = numerical_df.corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))

    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
        center=0, ax=ax, square=True, linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 7},
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_dir / "correlation_heatmap.png", dpi=FIG_DPI, bbox_inches="tight")

    return fig


def save_results(
    results: List[Dict[str, Any]],
    config: Dict[str, Any],
    project_root: Path = None,
    filename: str = "model_comparison.json",
) -> Path:
    """Save evaluation results to JSON.

    Args:
        results: List of evaluation result dictionaries.
        config: Project configuration.
        project_root: Project root directory.
        filename: Output filename.

    Returns:
        Path to saved results file.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent

    results_dir = project_root / config["artifacts"]["results_dir"]
    results_dir.mkdir(parents=True, exist_ok=True)

    # Make serializable
    serializable = []
    for r in results:
        entry = {k: v for k, v in r.items()
                 if k != "classification_report"}
        if "classification_report" in r:
            entry["classification_report"] = r["classification_report"]
        serializable.append(entry)

    filepath = results_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, default=str)

    logger.info("Results saved to %s", filepath)
    return filepath


def generate_all_plots(
    models: Dict[str, Any],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    results: List[Dict[str, Any]],
    config: Dict[str, Any],
    project_root: Path = None,
    df_full: pd.DataFrame = None,
) -> None:
    """Generate all evaluation plots and save them.

    Args:
        models: Dictionary of model name → fitted model.
        X_test: Test features.
        y_test: Test labels.
        results: Evaluation results.
        config: Project configuration.
        project_root: Project root directory.
        df_full: Full dataset for EDA plots.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent

    save_dir = project_root / config["artifacts"]["figures_dir"]
    save_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Generating evaluation plots...")

    plot_confusion_matrices(models, X_test, y_test, save_dir)
    plot_roc_curves(models, X_test, y_test, save_dir)
    plot_precision_recall_curves(models, X_test, y_test, save_dir)
    plot_calibration_curves(models, X_test, y_test, save_dir)
    plot_model_comparison_bars(results, save_dir)
    plot_class_distribution(y_test, "Test Set Class Distribution", save_dir)

    if df_full is not None:
        plot_correlation_heatmap(df_full, save_dir)

    plt.close("all")
    logger.info("All plots saved to %s", save_dir)
