"""
Unit Tests — Preprocessing Pipeline
=====================================
Tests data preprocessing, encoding, and scaling operations.
"""

import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import load_config
from src.preprocessing.pipeline import (
    drop_leakage_columns,
    drop_id_columns,
    encode_type_column,
    rename_columns,
)


@pytest.fixture
def config():
    """Load project configuration."""
    return load_config(str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))


@pytest.fixture
def sample_df():
    """Create a sample DataFrame matching AI4I schema."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "UDI": range(1, n + 1),
        "Product ID": [f"L{i}" for i in range(n)],
        "Type": np.random.choice(["L", "M", "H"], n),
        "Air temperature [K]": np.random.normal(300, 2, n),
        "Process temperature [K]": np.random.normal(310, 2, n),
        "Rotational speed [rpm]": np.random.randint(1200, 2000, n),
        "Torque [Nm]": np.random.normal(40, 10, n),
        "Tool wear [min]": np.random.randint(0, 240, n),
        "Machine failure": np.random.choice([0, 1], n, p=[0.966, 0.034]),
        "TWF": np.random.choice([0, 1], n, p=[0.99, 0.01]),
        "HDF": np.random.choice([0, 1], n, p=[0.99, 0.01]),
        "PWF": np.random.choice([0, 1], n, p=[0.99, 0.01]),
        "OSF": np.random.choice([0, 1], n, p=[0.99, 0.01]),
        "RNF": np.random.choice([0, 1], n, p=[0.99, 0.01]),
    })


class TestDropLeakageColumns:
    """Test leakage column removal."""

    def test_removes_failure_mode_columns(self, sample_df, config):
        result = drop_leakage_columns(sample_df, config)
        for col in ["TWF", "HDF", "PWF", "OSF", "RNF"]:
            assert col not in result.columns

    def test_preserves_target(self, sample_df, config):
        result = drop_leakage_columns(sample_df, config)
        assert "Machine failure" in result.columns

    def test_preserves_features(self, sample_df, config):
        result = drop_leakage_columns(sample_df, config)
        assert "Torque [Nm]" in result.columns


class TestDropIdColumns:
    """Test ID column removal."""

    def test_removes_udi_and_product_id(self, sample_df, config):
        result = drop_id_columns(sample_df, config)
        assert "UDI" not in result.columns
        assert "Product ID" not in result.columns


class TestEncodeTypeColumn:
    """Test ordinal encoding of Type column."""

    def test_encodes_correctly(self, config):
        df = pd.DataFrame({"Type": ["L", "M", "H", "L"]})
        result = encode_type_column(df, config)
        assert list(result["Type"]) == [0, 1, 2, 0]

    def test_handles_missing_column(self, config):
        df = pd.DataFrame({"other": [1, 2, 3]})
        result = encode_type_column(df, config)
        assert "other" in result.columns


class TestRenameColumns:
    """Test column renaming."""

    def test_renames_known_columns(self, sample_df, config):
        result = rename_columns(sample_df, config)
        assert "air_temp_k" in result.columns or "Air temperature [K]" not in result.columns
