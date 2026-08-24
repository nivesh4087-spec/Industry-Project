"""
Unit Tests — Risk Scoring
===========================
Tests risk score computation, categorization, and early warning.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import load_config
from src.risk.scoring import (
    compute_risk_score,
    get_risk_category,
    check_early_warning,
    PredictionHistory,
)


@pytest.fixture
def config():
    return load_config(str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))


class TestComputeRiskScore:
    """Test risk score computation."""

    def test_zero_probability(self, config):
        score = compute_risk_score(0.0, config)
        assert score == 0.0

    def test_one_probability(self, config):
        score = compute_risk_score(1.0, config)
        assert score == 100.0

    def test_mid_probability(self, config):
        score = compute_risk_score(0.5, config)
        assert 0 < score < 100

    def test_score_bounded(self, config):
        for prob in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
            score = compute_risk_score(prob, config)
            assert 0 <= score <= 100

    def test_clipping(self, config):
        score_neg = compute_risk_score(-0.1, config)
        score_over = compute_risk_score(1.5, config)
        assert score_neg == 0.0
        assert score_over == 100.0

    def test_monotonically_increasing(self, config):
        probs = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]
        scores = [compute_risk_score(p, config) for p in probs]
        for i in range(len(scores) - 1):
            assert scores[i] <= scores[i + 1]


class TestGetRiskCategory:
    """Test risk categorization."""

    def test_low_risk(self, config):
        cat = get_risk_category(20, config)
        assert "LOW" in cat["label"]

    def test_moderate_risk(self, config):
        cat = get_risk_category(45, config)
        assert "MODERATE" in cat["label"]

    def test_high_risk(self, config):
        cat = get_risk_category(70, config)
        assert "HIGH" in cat["label"]

    def test_critical_risk(self, config):
        cat = get_risk_category(95, config)
        assert "CRITICAL" in cat["label"]

    def test_boundary_low(self, config):
        cat = get_risk_category(30, config)
        assert "LOW" in cat["label"]

    def test_boundary_moderate(self, config):
        cat = get_risk_category(60, config)
        assert "MODERATE" in cat["label"]

    def test_category_has_color(self, config):
        cat = get_risk_category(50, config)
        assert "color" in cat
        assert cat["color"].startswith("#")


class TestEarlyWarning:
    """Test early warning trigger."""

    def test_triggers_above_threshold(self, config):
        assert check_early_warning(70, config) is True

    def test_no_trigger_below(self, config):
        assert check_early_warning(30, config) is False

    def test_boundary(self, config):
        threshold = config["early_warning"]["threshold"]
        assert check_early_warning(threshold, config) is True
        assert check_early_warning(threshold - 1, config) is False


class TestPredictionHistory:
    """Test prediction history tracking."""

    def test_add_prediction(self):
        history = PredictionHistory(max_entries=10)
        history.add_prediction(
            {"air_temp_k": 300},
            {
                "risk_score": 75,
                "failure_probability": 60,
                "risk_category": "HIGH RISK",
                "prediction": "FAILURE",
                "top_risk_factors": [{"feature": "torque"}],
            },
            ["Check torque"],
        )
        assert len(history.history) == 1

    def test_max_entries(self):
        history = PredictionHistory(max_entries=5)
        for i in range(10):
            history.add_prediction(
                {}, {
                    "risk_score": i * 10,
                    "failure_probability": i * 10,
                    "risk_category": "LOW RISK",
                    "prediction": "NO FAILURE",
                    "top_risk_factors": [],
                }, []
            )
        assert len(history.history) == 5

    def test_get_history_df(self):
        history = PredictionHistory()
        history.add_prediction(
            {}, {
                "risk_score": 50,
                "failure_probability": 40,
                "risk_category": "MODERATE RISK",
                "prediction": "NO FAILURE",
                "top_risk_factors": [],
            }, []
        )
        df = history.get_history_df()
        assert len(df) == 1
        assert "risk_score" in df.columns

    def test_alert_count(self):
        history = PredictionHistory()
        for cat in ["LOW RISK", "HIGH RISK", "CRITICAL RISK", "MODERATE RISK"]:
            history.add_prediction(
                {}, {
                    "risk_score": 50,
                    "failure_probability": 40,
                    "risk_category": cat,
                    "prediction": "NO FAILURE",
                    "top_risk_factors": [],
                }, []
            )
        assert history.get_alert_count() == 2  # HIGH + CRITICAL
