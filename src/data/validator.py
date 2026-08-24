"""
Data Validator Module
=====================
Validates schema, data quality, and class distribution of the AI4I 2020 dataset.

Performs:
- Schema validation (expected columns, types)
- Missing value detection
- Duplicate detection
- Range validation for continuous features
- Class distribution analysis
- Failure type breakdown
"""

import logging
from typing import Dict, Any, List, Tuple

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Expected schema for the AI4I 2020 dataset
EXPECTED_COLUMNS = [
    "UDI", "Product ID", "Type",
    "Air temperature [K]", "Process temperature [K]",
    "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]",
    "Machine failure", "TWF", "HDF", "PWF", "OSF", "RNF"
]

EXPECTED_RANGES = {
    "Air temperature [K]": (290.0, 310.0),
    "Process temperature [K]": (300.0, 320.0),
    "Rotational speed [rpm]": (1000, 3000),
    "Torque [Nm]": (3.0, 80.0),
    "Tool wear [min]": (0, 260),
}

FAILURE_COLUMNS = ["TWF", "HDF", "PWF", "OSF", "RNF"]


def validate_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate that the dataset has expected columns and types.

    Args:
        df: Loaded DataFrame.

    Returns:
        Validation report dictionary.
    """
    report = {
        "valid": True,
        "missing_columns": [],
        "extra_columns": [],
        "column_count_match": len(df.columns) == len(EXPECTED_COLUMNS),
    }

    # Map column aliases for flexible schema checking
    canonical_map = {
        "UID": "UDI", "UDI": "UDI",
        "Product ID": "Product ID",
        "Type": "Type",
        "Air temperature": "Air temperature [K]", "Air temperature [K]": "Air temperature [K]",
        "Process temperature": "Process temperature [K]", "Process temperature [K]": "Process temperature [K]",
        "Rotational speed": "Rotational speed [rpm]", "Rotational speed [rpm]": "Rotational speed [rpm]",
        "Torque": "Torque [Nm]", "Torque [Nm]": "Torque [Nm]",
        "Tool wear": "Tool wear [min]", "Tool wear [min]": "Tool wear [min]",
        "Machine failure": "Machine failure",
        "TWF": "TWF", "HDF": "HDF", "PWF": "PWF", "OSF": "OSF", "RNF": "RNF",
    }

    actual_canonical = {canonical_map.get(col, col) for col in df.columns}
    expected_cols = set(EXPECTED_COLUMNS)

    report["missing_columns"] = list(expected_cols - actual_canonical)

    if report["missing_columns"]:
        report["valid"] = False
        logger.warning("Missing columns: %s", report["missing_columns"])
    else:
        logger.info("Schema validation passed: all expected columns present.")

    return report


def validate_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
    """Check for missing values in the dataset.

    Args:
        df: Loaded DataFrame.

    Returns:
        Missing value report.
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    report = {
        "total_missing": int(missing.sum()),
        "columns_with_missing": {},
        "has_missing": bool(missing.sum() > 0),
    }

    for col in df.columns:
        if missing[col] > 0:
            report["columns_with_missing"][col] = {
                "count": int(missing[col]),
                "percentage": float(missing_pct[col]),
            }

    if report["has_missing"]:
        logger.warning(
            "Found %d missing values across %d columns.",
            report["total_missing"],
            len(report["columns_with_missing"])
        )
    else:
        logger.info("No missing values found.")

    return report


def validate_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """Check for duplicate rows in the dataset.

    Args:
        df: Loaded DataFrame.

    Returns:
        Duplicate report.
    """
    n_duplicates = int(df.duplicated().sum())
    n_duplicates_subset = int(
        df.drop(columns=["UDI", "Product ID"], errors="ignore").duplicated().sum()
    )

    report = {
        "total_duplicates": n_duplicates,
        "feature_duplicates": n_duplicates_subset,
        "has_duplicates": n_duplicates > 0,
    }

    logger.info(
        "Duplicates: %d exact, %d feature-only.",
        n_duplicates, n_duplicates_subset
    )

    return report


def validate_ranges(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate that numerical features are within expected ranges.

    Args:
        df: Loaded DataFrame.

    Returns:
        Range validation report with outlier counts.
    """
    report = {"columns": {}, "total_outliers": 0}

    for col, (low, high) in EXPECTED_RANGES.items():
        if col not in df.columns:
            continue

        below = int((df[col] < low).sum())
        above = int((df[col] > high).sum())
        outliers = below + above

        report["columns"][col] = {
            "expected_range": [low, high],
            "actual_min": round(float(df[col].min()), 4),
            "actual_max": round(float(df[col].max()), 4),
            "below_range": below,
            "above_range": above,
            "outliers": outliers,
        }
        report["total_outliers"] += outliers

    logger.info("Range validation complete. Total outliers: %d", report["total_outliers"])
    return report


def analyze_class_distribution(
    df: pd.DataFrame,
    target_col: str = "Machine failure"
) -> Dict[str, Any]:
    """Analyze the target variable class distribution.

    Args:
        df: Loaded DataFrame.
        target_col: Name of the target column.

    Returns:
        Class distribution report.
    """
    if target_col not in df.columns:
        logger.error("Target column '%s' not found.", target_col)
        return {"error": f"Column '{target_col}' not found"}

    counts = df[target_col].value_counts()
    percentages = (counts / len(df) * 100).round(2)

    report = {
        "target_column": target_col,
        "class_counts": counts.to_dict(),
        "class_percentages": {str(k): float(v) for k, v in percentages.items()},
        "imbalance_ratio": round(float(counts.max() / counts.min()), 2),
        "minority_class": int(counts.idxmin()),
        "majority_class": int(counts.idxmax()),
        "is_imbalanced": float(counts.min() / counts.max()) < 0.2,
    }

    logger.info(
        "Class distribution — No Failure: %d (%.1f%%), Failure: %d (%.1f%%). "
        "Imbalance ratio: %.1f:1",
        counts.get(0, 0), percentages.get(0, 0),
        counts.get(1, 0), percentages.get(1, 0),
        report["imbalance_ratio"]
    )

    return report


def analyze_failure_types(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze individual failure type distributions.

    Args:
        df: Loaded DataFrame.

    Returns:
        Failure type breakdown report.
    """
    report = {"failure_types": {}, "total_failures": 0}

    for col in FAILURE_COLUMNS:
        if col not in df.columns:
            continue

        count = int(df[col].sum())
        pct = round(count / len(df) * 100, 3)
        report["failure_types"][col] = {
            "count": count,
            "percentage": pct,
            "full_name": {
                "TWF": "Tool Wear Failure",
                "HDF": "Heat Dissipation Failure",
                "PWF": "Power Failure",
                "OSF": "Overstrain Failure",
                "RNF": "Random Failure",
            }.get(col, col),
        }

    if "Machine failure" in df.columns:
        report["total_failures"] = int(df["Machine failure"].sum())

    logger.info(
        "Failure types: %s",
        {k: v["count"] for k, v in report["failure_types"].items()}
    )

    return report


def run_full_validation(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Run all validation checks and return a comprehensive report.

    Args:
        df: Loaded DataFrame.
        config: Project configuration.

    Returns:
        Complete validation report.
    """
    target_col = config["data"]["target_column"]

    report = {
        "schema": validate_schema(df),
        "missing_values": validate_missing_values(df),
        "duplicates": validate_duplicates(df),
        "ranges": validate_ranges(df),
        "class_distribution": analyze_class_distribution(df, target_col),
        "failure_types": analyze_failure_types(df),
        "overall_valid": True,
    }

    # Determine overall validity
    if not report["schema"]["valid"]:
        report["overall_valid"] = False
    if report["missing_values"]["has_missing"]:
        logger.warning("Dataset has missing values — may require imputation.")

    logger.info("Full validation complete. Overall valid: %s", report["overall_valid"])
    return report
