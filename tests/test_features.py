"""
Unit Tests — Feature Engineering
==================================
Tests engineered feature correctness and documentation.
"""

import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import load_config
from src.features.engineer import (
    engineer_features,
    get_feature_documentation,
    get_all_feature_names,
)


@pytest.fixture
def config():
    return load_config(str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))


@pytest.fixture
def sample_features():
    """Create a sample feature DataFrame."""
    np.random.seed(42)
    n = 50
    return pd.DataFrame({
        "type": np.random.choice([0, 1, 2], n),
        "air_temp_k": np.random.normal(300, 2, n),
        "process_temp_k": np.random.normal(310, 2, n),
        "rotational_speed_rpm": np.random.randint(1200, 2000, n),
        "torque_nm": np.random.normal(40, 10, n),
        "tool_wear_min": np.random.randint(0, 240, n),
    })


class TestEngineerFeatures:
    """Test feature engineering logic."""

    def test_creates_expected_features(self, sample_features, config):
        result, stats = engineer_features(sample_features, config)
        expected = [
            "temp_diff", "power", "torque_per_rpm", "strain",
            "power_factor", "temp_rpm_interaction", "tool_wear_severity",
            "is_high_torque", "is_low_speed", "overload_indicator"
        ]
        for feat in expected:
            assert feat in result.columns, f"Missing feature: {feat}"

    def test_temp_diff_calculation(self, sample_features, config):
        result, _ = engineer_features(sample_features, config)
        expected = sample_features["process_temp_k"] - sample_features["air_temp_k"]
        np.testing.assert_array_almost_equal(result["temp_diff"].values, expected.values)

    def test_strain_calculation(self, sample_features, config):
        result, _ = engineer_features(sample_features, config)
        expected = sample_features["tool_wear_min"] * sample_features["torque_nm"]
        np.testing.assert_array_almost_equal(result["strain"].values, expected.values)

    def test_binary_features_are_binary(self, sample_features, config):
        result, _ = engineer_features(sample_features, config)
        for col in ["is_high_torque", "is_low_speed", "overload_indicator"]:
            assert set(result[col].unique()).issubset({0, 1})

    def test_no_nulls_created(self, sample_features, config):
        result, _ = engineer_features(sample_features, config)
        assert result.isnull().sum().sum() == 0

    def test_stats_returned(self, sample_features, config):
        _, stats = engineer_features(sample_features, config)
        assert "torque_q75" in stats
        assert "rpm_q25" in stats

    def test_stats_applied_correctly(self, sample_features, config):
        """Test that pre-computed stats override computation."""
        _, train_stats = engineer_features(sample_features, config)
        # Apply same stats to new data
        new_data = sample_features.copy()
        result, _ = engineer_features(new_data, config, fit_stats=train_stats)
        # Should still have all features
        assert "is_high_torque" in result.columns


class TestFeatureDocumentation:
    """Test feature documentation completeness."""

    def test_all_features_documented(self):
        docs = get_feature_documentation()
        expected = [
            "temp_diff", "power", "torque_per_rpm", "strain",
            "power_factor", "temp_rpm_interaction", "tool_wear_severity",
            "is_high_torque", "is_low_speed", "overload_indicator"
        ]
        for feat in expected:
            assert feat in docs, f"Missing documentation for: {feat}"

    def test_docs_have_required_fields(self):
        docs = get_feature_documentation()
        for name, doc in docs.items():
            assert "formula" in doc, f"{name} missing formula"
            assert "rationale" in doc, f"{name} missing rationale"
            assert "interpretation" in doc, f"{name} missing interpretation"


class TestGetAllFeatureNames:
    """Test feature name listing."""

    def test_base_features(self):
        names = get_all_feature_names(include_engineered=False)
        assert len(names) == 6
        assert "air_temp_k" in names

    def test_all_features(self):
        names = get_all_feature_names(include_engineered=True)
        assert len(names) == 16
        assert "temp_diff" in names
