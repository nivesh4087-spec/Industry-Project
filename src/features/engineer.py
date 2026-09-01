"""
Feature Engineering Module
==========================
Creates physically-meaningful engineered features from the AI4I 2020 dataset.

Each feature is documented with:
- Formula
- Physical rationale
- Expected interpretation

IMPORTANT: All features are derived from known physical relationships
in manufacturing processes. They are NOT random combinations.
"""

import logging
from typing import Dict, Any, List, Tuple

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Feature Engineering Documentation
FEATURE_DOCS = {
    "temp_diff": {
        "formula": "process_temp_k - air_temp_k",
        "rationale": (
            "Temperature difference between process and ambient indicates "
            "heat dissipation effectiveness. Higher differences suggest "
            "thermal stress or inadequate cooling."
        ),
        "unit": "K",
        "interpretation": "Higher values → potential heat dissipation failure",
    },
    "power": {
        "formula": "torque_nm × rotational_speed_rpm × 2π / 60",
        "rationale": (
            "Mechanical power output (Watts). P = τ × ω where τ is torque "
            "and ω is angular velocity. Extreme power indicates overloading."
        ),
        "unit": "W",
        "interpretation": "Very high or low values → abnormal operation",
    },
    "torque_per_rpm": {
        "formula": "torque_nm / rotational_speed_rpm",
        "rationale": (
            "Load efficiency — how much torque is needed per unit speed. "
            "High ratios suggest mechanical resistance or load issues."
        ),
        "unit": "Nm/rpm",
        "interpretation": "High values → excessive load per rotation",
    },
    "strain": {
        "formula": "tool_wear_min × torque_nm",
        "rationale": (
            "Combined mechanical strain — worn tools under high torque "
            "are more likely to cause failures. This interaction captures "
            "the compounding effect of wear and load."
        ),
        "unit": "min·Nm",
        "interpretation": "High values → compounded wear-load risk",
    },
    "power_factor": {
        "formula": "torque_nm × rotational_speed_rpm",
        "rationale": (
            "Simplified power proxy (proportional to mechanical power). "
            "Useful as a single feature capturing the torque-speed relationship."
        ),
        "unit": "Nm·rpm",
        "interpretation": "Extreme values → power anomaly",
    },
    "temp_rpm_interaction": {
        "formula": "temp_diff × rotational_speed_rpm",
        "rationale": (
            "Thermal-speed stress interaction. High temperatures at high "
            "speeds create compounded stress on machinery."
        ),
        "unit": "K·rpm",
        "interpretation": "High values → thermal-mechanical stress",
    },
    "tool_wear_severity": {
        "formula": "Binned tool_wear_min: [0-50]=Low, [50-100]=Medium, [100-175]=High, [175+]=Critical",
        "rationale": (
            "Non-linear binning of tool wear. The effect of tool wear on "
            "failure risk is not linear — degradation accelerates with age."
        ),
        "unit": "Category",
        "interpretation": "Higher severity → higher failure risk",
    },
    "is_high_torque": {
        "formula": "1 if torque_nm > 75th percentile, else 0",
        "rationale": (
            "Binary flag for high-load conditions. Sustained high torque "
            "accelerates mechanical wear."
        ),
        "unit": "Binary",
        "interpretation": "1 → machine operating under high load",
    },
    "is_low_speed": {
        "formula": "1 if rotational_speed_rpm < 25th percentile, else 0",
        "rationale": (
            "Binary flag for abnormally low speed. May indicate power supply "
            "issues or mechanical resistance."
        ),
        "unit": "Binary",
        "interpretation": "1 → abnormal low-speed operation",
    },
    "overload_indicator": {
        "formula": "1 if (torque > 75th pct) AND (rpm < 25th pct), else 0",
        "rationale": (
            "Overstrain detection — high torque combined with low speed "
            "is a classic overstrain pattern in rotating machinery."
        ),
        "unit": "Binary",
        "interpretation": "1 → overstrain condition detected",
    },
}


def engineer_features(
    df: pd.DataFrame,
    config: Dict[str, Any],
    fit_stats: Dict[str, float] = None,
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Create all engineered features from raw dataset columns.

    IMPORTANT: Percentile thresholds are computed from training data only
    to prevent data leakage. Pass fit_stats from training set when
    transforming validation/test sets.

    Args:
        df: DataFrame with cleaned column names.
        config: Project configuration.
        fit_stats: Pre-computed statistics (percentiles) from training data.
                   If None, computes from the provided DataFrame (training mode).

    Returns:
        Tuple of (DataFrame with engineered features, fit statistics dict).
    """
    df = df.copy()
    stats = fit_stats or {}

    # --- Continuous Engineered Features ---

    # 1. Temperature difference (heat dissipation indicator)
    df["temp_diff"] = df["process_temp_k"] - df["air_temp_k"]

    # 2. Mechanical power output (Watts): P = τ × ω
    df["power"] = df["torque_nm"] * df["rotational_speed_rpm"] * 2 * np.pi / 60

    # 3. Torque per RPM (load efficiency)
    # Add small epsilon to avoid division by zero
    df["torque_per_rpm"] = df["torque_nm"] / (df["rotational_speed_rpm"] + 1e-6)

    # 4. Combined strain (wear × torque interaction)
    df["strain"] = df["tool_wear_min"] * df["torque_nm"]

    # 5. Power factor (torque × speed proxy)
    df["power_factor"] = df["torque_nm"] * df["rotational_speed_rpm"]

    # 6. Temperature-speed interaction (temp_diff already computed above)
    df["temp_rpm_interaction"] = df["temp_diff"] * df["rotational_speed_rpm"]

    # --- Binned / Categorical Features ---

    # 7. Tool wear severity (non-linear binning)
    # boundaries define the bin edges: [0, 50, 100, 175, 250]
    # We replace the last edge with np.inf so all values >= 175 are 'critical'
    bins = config["features"]["tool_wear_bins"]["boundaries"]
    labels_list = config["features"]["tool_wear_bins"]["labels"]
    # Need len(labels) + 1 bin edges. boundaries has 5 edges → 4 intervals → 4 labels ✓
    bin_edges = bins[:-1] + [np.inf]  # [0, 50, 100, 175, inf]
    df["tool_wear_severity"] = pd.cut(
        df["tool_wear_min"],
        bins=bin_edges,
        labels=labels_list,
        right=True,
        include_lowest=True,
    )
    # Convert to ordinal encoding
    severity_map = {label: i for i, label in enumerate(labels_list)}
    df["tool_wear_severity"] = df["tool_wear_severity"].map(severity_map).fillna(0).astype(int)

    # --- Threshold-based Binary Features ---
    # Compute thresholds from data (training mode) or use pre-computed

    if "torque_q75" not in stats:
        # Training mode: compute statistics
        stats["torque_q75"] = float(df["torque_nm"].quantile(0.75))
        stats["rpm_q25"] = float(df["rotational_speed_rpm"].quantile(0.25))
        logger.info(
            "Computed feature thresholds — torque_q75: %.2f, rpm_q25: %.2f",
            stats["torque_q75"], stats["rpm_q25"]
        )

    # 8. High torque flag
    df["is_high_torque"] = (df["torque_nm"] > stats["torque_q75"]).astype(int)

    # 9. Low speed flag
    df["is_low_speed"] = (df["rotational_speed_rpm"] < stats["rpm_q25"]).astype(int)

    # 10. Overload indicator (high torque + low speed)
    df["overload_indicator"] = (
        (df["torque_nm"] > stats["torque_q75"]) &
        (df["rotational_speed_rpm"] < stats["rpm_q25"])
    ).astype(int)

    logger.info(
        "Engineered %d new features: %s",
        10,
        ["temp_diff", "power", "torque_per_rpm", "strain", "power_factor",
         "temp_rpm_interaction", "tool_wear_severity", "is_high_torque",
         "is_low_speed", "overload_indicator"]
    )

    return df, stats


def get_feature_documentation() -> Dict[str, Dict[str, str]]:
    """Return documentation for all engineered features.

    Returns:
        Dictionary mapping feature names to their documentation.
    """
    return FEATURE_DOCS


def get_all_feature_names(include_engineered: bool = True) -> List[str]:
    """Get the complete list of feature names used for modeling.

    Args:
        include_engineered: Whether to include engineered features.

    Returns:
        List of feature column names.
    """
    base_features = [
        "type", "air_temp_k", "process_temp_k",
        "rotational_speed_rpm", "torque_nm", "tool_wear_min"
    ]

    if not include_engineered:
        return base_features

    engineered = [
        "temp_diff", "power", "torque_per_rpm", "strain",
        "power_factor", "temp_rpm_interaction", "tool_wear_severity",
        "is_high_torque", "is_low_speed", "overload_indicator"
    ]

    return base_features + engineered


def generate_feature_report(
    df: pd.DataFrame,
    stats: Dict[str, float]
) -> Dict[str, Any]:
    """Generate a summary report of engineered features.

    Args:
        df: DataFrame with engineered features.
        stats: Fit statistics used for threshold features.

    Returns:
        Feature engineering report dictionary.
    """
    engineered_cols = [
        "temp_diff", "power", "torque_per_rpm", "strain",
        "power_factor", "temp_rpm_interaction", "tool_wear_severity",
        "is_high_torque", "is_low_speed", "overload_indicator"
    ]

    report = {
        "total_engineered": len(engineered_cols),
        "fit_statistics": stats,
        "feature_stats": {},
        "documentation": FEATURE_DOCS,
    }

    for col in engineered_cols:
        if col in df.columns:
            report["feature_stats"][col] = {
                "mean": round(float(df[col].mean()), 4),
                "std": round(float(df[col].std()), 4),
                "min": round(float(df[col].min()), 4),
                "max": round(float(df[col].max()), 4),
                "nulls": int(df[col].isnull().sum()),
            }

    return report
