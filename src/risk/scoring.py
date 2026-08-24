"""
Risk Scoring Module
===================
Transforms model predictions into interpretable risk scores and categories.

Risk Score:
- 0–30: LOW RISK 🟢
- 31–60: MODERATE RISK 🟡
- 61–80: HIGH RISK 🟠
- 81–100: CRITICAL RISK 🔴

The risk score uses a non-linear transform of the calibrated failure probability
to amplify moderate risks. The exact thresholds are configurable and documented
as engineering defaults, NOT scientifically validated values.

Early Warning System:
- Triggers when risk score exceeds a configurable threshold.
- Provides machine status, risk level, top contributing features, and actions.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def compute_risk_score(
    failure_probability: float,
    config: Dict[str, Any],
) -> float:
    """Transform failure probability into a 0-100 risk score.

    Uses a non-linear power transform: risk_score = probability^exponent × 100
    The exponent < 1 amplifies moderate probabilities, making the system
    more sensitive to moderate-risk conditions.

    NOTE: This is an engineering design choice, not a validated scientific formula.

    Args:
        failure_probability: Calibrated failure probability (0-1).
        config: Project configuration.

    Returns:
        Risk score in [0, 100].
    """
    prob = np.clip(failure_probability, 0.0, 1.0)
    exponent = config["risk"]["transform_exponent"]

    risk_score = (prob ** exponent) * 100
    risk_score = np.clip(risk_score, 0.0, 100.0)

    return round(float(risk_score), 1)


def get_risk_category(
    risk_score: float,
    config: Dict[str, Any],
) -> Dict[str, str]:
    """Classify risk score into a category.

    Args:
        risk_score: Risk score (0-100).
        config: Project configuration.

    Returns:
        Dictionary with category label, color, and emoji.
    """
    thresholds = config["risk"]["thresholds"]
    categories = config["risk"]["categories"]

    if risk_score <= thresholds["low"]:
        return categories["low"]
    elif risk_score <= thresholds["moderate"]:
        return categories["moderate"]
    elif risk_score <= thresholds["high"]:
        return categories["high"]
    else:
        return categories["critical"]


def generate_risk_assessment(
    failure_probability: float,
    shap_explanation: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate a complete risk assessment for a prediction.

    Combines:
    - Risk score
    - Risk category
    - Failure probability
    - Top risk factors from SHAP
    - Overall assessment

    Args:
        failure_probability: Calibrated failure probability.
        shap_explanation: SHAP explanation from SHAPEngine.
        config: Project configuration.

    Returns:
        Complete risk assessment dictionary.
    """
    risk_score = compute_risk_score(failure_probability, config)
    category = get_risk_category(risk_score, config)

    assessment = {
        "timestamp": datetime.now().isoformat(),
        "failure_probability": round(float(failure_probability) * 100, 1),
        "risk_score": risk_score,
        "risk_category": category["label"],
        "risk_color": category["color"],
        "risk_emoji": category["emoji"],
        "prediction": "FAILURE" if failure_probability >= 0.5 else "NO FAILURE",
        "top_risk_factors": [],
        "assessment_summary": "",
    }

    # Extract top risk factors from SHAP
    if "top_factors" in shap_explanation:
        for factor in shap_explanation["top_factors"][:5]:
            assessment["top_risk_factors"].append({
                "feature": factor["feature"],
                "value": factor["value"],
                "impact": factor["impact"],
                "importance": round(factor["abs_importance"], 4),
            })

    # Generate summary
    if risk_score <= 30:
        assessment["assessment_summary"] = (
            "Machine is operating within normal parameters. "
            "No immediate action required. Continue routine monitoring."
        )
    elif risk_score <= 60:
        assessment["assessment_summary"] = (
            "Machine shows elevated risk indicators. "
            "Schedule preventive inspection at next maintenance window."
        )
    elif risk_score <= 80:
        assessment["assessment_summary"] = (
            "Machine is at HIGH RISK of failure. "
            "Prioritize inspection and address contributing factors."
        )
    else:
        assessment["assessment_summary"] = (
            "CRITICAL: Machine has a very high probability of failure. "
            "Immediate inspection and corrective action recommended."
        )

    return assessment


def check_early_warning(
    risk_score: float,
    config: Dict[str, Any],
) -> bool:
    """Check if the risk score triggers an early warning.

    Args:
        risk_score: Computed risk score (0-100).
        config: Project configuration.

    Returns:
        True if early warning should be triggered.
    """
    threshold = config["early_warning"]["threshold"]
    return risk_score >= threshold


def generate_early_warning(
    risk_assessment: Dict[str, Any],
    config: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Generate an early warning alert if conditions are met.

    Args:
        risk_assessment: Complete risk assessment.
        config: Project configuration.

    Returns:
        Early warning alert dictionary, or None if not triggered.
    """
    if not check_early_warning(risk_assessment["risk_score"], config):
        return None

    warning = {
        "type": "EARLY WARNING",
        "severity": risk_assessment["risk_category"],
        "timestamp": risk_assessment["timestamp"],
        "risk_score": risk_assessment["risk_score"],
        "failure_probability": risk_assessment["failure_probability"],
        "top_contributing_features": [],
        "recommended_action": "",
        "message": "",
    }

    # Extract main contributing features
    for factor in risk_assessment["top_risk_factors"][:3]:
        if factor["impact"] == "increases risk":
            warning["top_contributing_features"].append(factor["feature"])

    # Build warning message
    if warning["top_contributing_features"]:
        factors_str = ", ".join(warning["top_contributing_features"])
        warning["message"] = (
            f"⚠ EARLY WARNING — Risk Score: {risk_assessment['risk_score']}/100 | "
            f"Primary factors: {factors_str}"
        )
    else:
        warning["message"] = (
            f"⚠ EARLY WARNING — Risk Score: {risk_assessment['risk_score']}/100 | "
            "Review machine parameters."
        )

    return warning


# ============================================================================
# Prediction History
# ============================================================================

class PredictionHistory:
    """Maintains a history of predictions for monitoring and alerting.

    Stores predictions in memory with a configurable maximum size.
    """

    def __init__(self, max_entries: int = 500):
        """Initialize prediction history.

        Args:
            max_entries: Maximum number of entries to retain.
        """
        self.max_entries = max_entries
        self.history: List[Dict[str, Any]] = []

    def add_prediction(
        self,
        input_data: Dict[str, float],
        risk_assessment: Dict[str, Any],
        recommendations: List[str],
    ) -> None:
        """Add a prediction to history.

        Args:
            input_data: Raw input parameters.
            risk_assessment: Complete risk assessment.
            recommendations: List of recommendations.
        """
        entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_data": input_data,
            "risk_score": risk_assessment["risk_score"],
            "failure_probability": risk_assessment["failure_probability"],
            "risk_category": risk_assessment["risk_category"],
            "prediction": risk_assessment["prediction"],
            "top_factor": (
                risk_assessment["top_risk_factors"][0]["feature"]
                if risk_assessment["top_risk_factors"]
                else "N/A"
            ),
            "recommendation": recommendations[0] if recommendations else "No action required",
        }

        self.history.append(entry)

        # Trim to max entries
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]

    def get_history_df(self) -> pd.DataFrame:
        """Get prediction history as a DataFrame.

        Returns:
            DataFrame with prediction history.
        """
        if not self.history:
            return pd.DataFrame(columns=[
                "id", "timestamp", "risk_score", "failure_probability",
                "risk_category", "prediction", "top_factor", "recommendation"
            ])

        return pd.DataFrame(self.history)

    def get_alert_count(self) -> int:
        """Get count of high-risk predictions.

        Returns:
            Number of high or critical risk predictions.
        """
        return sum(
            1 for h in self.history
            if h["risk_category"] in ["HIGH RISK", "CRITICAL RISK"]
        )

    def get_risk_distribution(self) -> Dict[str, int]:
        """Get distribution of risk categories.

        Returns:
            Dictionary mapping risk category to count.
        """
        distribution = {
            "LOW RISK": 0,
            "MODERATE RISK": 0,
            "HIGH RISK": 0,
            "CRITICAL RISK": 0,
        }
        for h in self.history:
            cat = h.get("risk_category", "")
            if cat in distribution:
                distribution[cat] += 1
        return distribution
