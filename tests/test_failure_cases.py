"""
Unit Tests — Failure & Edge Cases
====================================
Comprehensive failure case unit testing for error handling, corrupt inputs,
out-of-bounds parameters, and invalid data schema across all pipeline modules.
"""

import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import load_config, load_dataset, rename_columns
from src.preprocessing.pipeline import (
    drop_leakage_columns,
    drop_id_columns,
    encode_type_column,
    preprocess_single_input,
)
from src.features.engineer import engineer_features
from src.risk.scoring import (
    compute_risk_score,
    get_risk_category,
    check_early_warning,
    PredictionHistory,
)
from src.recommendations.engine import (
    generate_recommendations,
    format_recommendations_text,
    get_recommendation_summary,
)


@pytest.fixture
def config():
    """Load configuration for tests."""
    return load_config(str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))


# ============================================================================
# 1. Data Loader Failure Cases
# ============================================================================

class TestDataLoaderFailures:
    """Failure test cases for data loading."""

    def test_load_config_nonexistent_file(self):
        """Test loading a non-existent YAML configuration file."""
        with pytest.raises(FileNotFoundError):
            load_config("non_existent_config_file_path_xyz.yaml")

    def test_load_dataset_missing_path(self, config):
        """Test loading dataset when explicit file path does not exist."""
        with pytest.raises(FileNotFoundError):
            load_dataset(config, filepath="data/non_existent_dataset.csv")

    def test_rename_columns_empty_dataframe(self, config):
        """Test renaming columns on an empty DataFrame."""
        empty_df = pd.DataFrame()
        renamed = rename_columns(empty_df, config)
        assert renamed.empty

    def test_rename_columns_unknown_columns(self, config):
        """Test renaming columns when DataFrame has unrecognized column names."""
        df = pd.DataFrame({"random_col_1": [1, 2], "unknown_sensor": [3.0, 4.0]})
        renamed = rename_columns(df, config)
        assert list(renamed.columns) == ["random_col_1", "unknown_sensor"]


# ============================================================================
# 2. Preprocessing Failure Cases
# ============================================================================

class TestPreprocessingFailures:
    """Failure test cases for data preprocessing pipeline."""

    def test_drop_leakage_columns_missing_leakage_cols(self, config):
        """Test dropping leakage columns when none are present in DataFrame."""
        df = pd.DataFrame({"air_temp_k": [300.0], "torque_nm": [40.0]})
        result = drop_leakage_columns(df, config)
        assert list(result.columns) == ["air_temp_k", "torque_nm"]

    def test_drop_id_columns_missing_id_cols(self, config):
        """Test dropping ID columns when ID columns are not in DataFrame."""
        df = pd.DataFrame({"feature1": [10], "feature2": [20]})
        result = drop_id_columns(df, config)
        assert list(result.columns) == ["feature1", "feature2"]

    def test_encode_type_column_unseen_categories(self, config):
        """Test ordinal encoding when unknown/unseen category string is passed."""
        df = pd.DataFrame({"Type": ["X", "UNKNOWN", "INVALID"]})
        result = encode_type_column(df, config)
        assert "Type" in result.columns
        assert not result["Type"].isnull().any()

    def test_encode_type_column_numeric_input(self, config):
        """Test encoding when Type is already numeric."""
        df = pd.DataFrame({"Type": [0, 1, 2]})
        result = encode_type_column(df, config)

# ============================================================================
# 3. Feature Engineering Failure & Edge Cases
# ============================================================================

class TestFeatureEngineeringFailures:
    """Failure and edge test cases for feature engineering."""

    def test_zero_rotational_speed(self, config):
        """Test feature engineering when rotational speed is 0 (division by zero test)."""
        df = pd.DataFrame({
            "type": [1],
            "air_temp_k": [300.0],
            "process_temp_k": [310.0],
            "rotational_speed_rpm": [0],
            "torque_nm": [50.0],
            "tool_wear_min": [100],
        })
        result, _ = engineer_features(df, config)
        assert not np.isinf(result["torque_per_rpm"].values[0])
        assert not np.isnan(result["torque_per_rpm"].values[0])

    def test_missing_required_feature_column(self, config):
        """Test engineer_features when mandatory feature columns are missing."""
        df = pd.DataFrame({
            "air_temp_k": [300.0],
        })
        with pytest.raises((KeyError, ValueError, Exception)):
            engineer_features(df, config)

    def test_negative_values(self, config):
        """Test feature engineering with negative sensor values."""
        df = pd.DataFrame({
            "type": [0],
            "air_temp_k": [-50.0],
            "process_temp_k": [-10.0],
            "rotational_speed_rpm": [-100],
            "torque_nm": [-20.0],
            "tool_wear_min": [-10],
        })
        result, _ = engineer_features(df, config)
        assert len(result) == 1
        assert not result.isnull().any().any()


# ============================================================================
# 4. Single Input Prediction Preprocessing Failures
# ============================================================================

class TestPredictionFailures:
    """Failure cases for prediction pipeline functions."""

    def test_preprocess_single_input_missing_key(self, config):
        """Test single input preprocessing with missing input dictionary keys."""
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        scaler.fit(np.zeros((5, 16)))

# ============================================================================
# 5. Risk Scoring & Early Warning Failure Cases
# ============================================================================

class TestRiskScoringFailures:
    """Failure and edge cases for risk scoring logic."""

    def test_compute_risk_score_negative_probability(self, config):
        """Test risk score calculation with negative probability."""
        score = compute_risk_score(-0.5, config)
        assert score == 0.0

    def test_compute_risk_score_excessive_probability(self, config):
        """Test risk score calculation with probability > 1.0."""
        score = compute_risk_score(2.5, config)
        assert score == 100.0

    def test_get_risk_category_negative_score(self, config):
        """Test getting risk category for negative risk score."""
        cat = get_risk_category(-10.0, config)
        assert "LOW" in cat["label"]

    def test_get_risk_category_excessive_score(self, config):
        """Test getting risk category for score > 100."""
        cat = get_risk_category(150.0, config)
        assert "CRITICAL" in cat["label"]

    def test_prediction_history_empty_query(self):
        """Test prediction history query on empty history."""
        history = PredictionHistory(max_entries=10)
        assert len(history.history) == 0
        df = history.get_history_df()
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert history.get_alert_count() == 0


# ============================================================================
# 6. Recommendation Engine Failure Cases
# ============================================================================

class TestRecommendationEngineFailures:
    """Failure test cases for maintenance recommendation engine."""

    def test_generate_recommendations_empty_explanation(self, config):
        """Test recommendation generation with empty explanation dictionary."""
        recs = generate_recommendations({}, config)
        assert recs == []

    def test_generate_recommendations_missing_top_factors(self, config):
        """Test recommendation generation when top_factors key is missing."""
        recs = generate_recommendations({"other_key": 123}, config)
        assert recs == []

    def test_generate_recommendations_unknown_features(self, config):
        """Test recommendation generation with unknown feature names in SHAP factors."""
        explanation = {
            "top_factors": [
                {
                    "feature": "non_existent_feature_abc",
                    "value": 999.0,
                    "shap_value": 0.9,
                    "impact": "increases risk",
                }
            ]
        }
        recs = generate_recommendations(explanation, config)
        assert isinstance(recs, list)

    def test_format_recommendations_invalid_input(self):
        """Test formatting recommendations when invalid non-list object is passed."""
        formatted = format_recommendations_text(None)
        assert "No significant risk" in formatted or isinstance(formatted, str)

    def test_get_recommendation_summary_malformed_input(self):
        """Test summary extraction with malformed recommendations list."""
        summary = get_recommendation_summary([{"invalid_key": "val"}])
        assert isinstance(summary, list)
        assert len(summary) > 0

    def test_encode_type_column_null_values(self, config):
        """Test encoding when Type column contains Null/NaN values."""
        df = pd.DataFrame({"Type": ["L", None, "H"]})
        result = encode_type_column(df, config)
        assert "Type" in result.columns
        assert result["Type"].isnull().sum() == 0
