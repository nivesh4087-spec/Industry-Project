"""
Unit Tests — Prediction Pipeline
===================================
Tests the end-to-end prediction pipeline including single input processing.
"""

import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import load_config
from src.features.engineer import engineer_features
from src.preprocessing.pipeline import preprocess_single_input
from sklearn.preprocessing import StandardScaler


@pytest.fixture
def config():
    return load_config(str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))


@pytest.fixture
def mock_pipeline(config):
    """Create a mock preprocessing pipeline with fitted components."""
    # Create sample training data
    np.random.seed(42)
    n = 100
    df = pd.DataFrame({
        "type": np.random.choice([0, 1, 2], n),
        "air_temp_k": np.random.normal(300, 2, n),
        "process_temp_k": np.random.normal(310, 2, n),
        "rotational_speed_rpm": np.random.randint(1200, 2000, n),
        "torque_nm": np.random.normal(40, 10, n),
        "tool_wear_min": np.random.randint(0, 240, n),
    })

    # Engineer features
    df_eng, stats = engineer_features(df, config)

    # Fit scaler
    numerical_cols = df_eng.select_dtypes(include=[np.number]).columns.tolist()
    scaler = StandardScaler()
    scaler.fit(df_eng[numerical_cols])

    feature_names = list(df_eng.columns)

    return {
        "scaler": scaler,
        "feature_stats": stats,
        "feature_names": feature_names,
        "numerical_cols": numerical_cols,
    }


class TestPreprocessSingleInput:
    """Test single input preprocessing for dashboard predictions."""

    def test_output_shape(self, config, mock_pipeline):
        input_data = {
            "air_temp_k": 300.0,
            "process_temp_k": 310.0,
            "rotational_speed_rpm": 1500,
            "torque_nm": 40.0,
            "tool_wear_min": 100,
            "type": 1,
        }

        result = preprocess_single_input(
            input_data, config,
            mock_pipeline["scaler"],
            mock_pipeline["feature_stats"],
            mock_pipeline["feature_names"],
            mock_pipeline["numerical_cols"],
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert len(result.columns) == len(mock_pipeline["feature_names"])

    def test_no_nulls(self, config, mock_pipeline):
        input_data = {
            "air_temp_k": 298.5,
            "process_temp_k": 308.7,
            "rotational_speed_rpm": 1500,
            "torque_nm": 40.0,
            "tool_wear_min": 30,
            "type": 1,
        }

        result = preprocess_single_input(
            input_data, config,
            mock_pipeline["scaler"],
            mock_pipeline["feature_stats"],
            mock_pipeline["feature_names"],
            mock_pipeline["numerical_cols"],
        )

        assert result.isnull().sum().sum() == 0

    def test_column_order_matches(self, config, mock_pipeline):
        input_data = {
            "air_temp_k": 300.0,
            "process_temp_k": 310.0,
            "rotational_speed_rpm": 1500,
            "torque_nm": 40.0,
            "tool_wear_min": 100,
            "type": 1,
        }

        result = preprocess_single_input(
            input_data, config,
            mock_pipeline["scaler"],
            mock_pipeline["feature_stats"],
            mock_pipeline["feature_names"],
            mock_pipeline["numerical_cols"],
        )

        assert list(result.columns) == mock_pipeline["feature_names"]
