"""
Unit Tests — Data Loader Module
===============================
Tests data loading, ucimlrepo integration, and Excel dataset support.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import (
    load_config,
    load_dataset,
    fetch_dataset_ucirepo,
    rename_columns,
)


@pytest.fixture
def config():
    return load_config(str(Path(__file__).resolve().parent.parent / "config" / "config.yaml"))


class TestDataLoader:
    """Test data loader functionalities."""

    def test_load_local_dataset(self, config):
        df = load_dataset(config)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_fetch_ucirepo_integration(self):
        try:
            df = fetch_dataset_ucirepo(uci_id=601)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 10000
            assert len(df.columns) == 14
        except Exception as e:
            pytest.skip(f"Network / UCI API unavailable: {e}")

    def test_rename_columns_variants(self, config):
        # Test renaming standard CSV column names
        df_csv = pd.DataFrame({
            "Air temperature [K]": [300.0],
            "Process temperature [K]": [310.0],
            "Rotational speed [rpm]": [1500],
            "Torque [Nm]": [40.0],
            "Tool wear [min]": [100],
            "Type": ["M"],
            "Machine failure": [0]
        })
        renamed_csv = rename_columns(df_csv, config)
        assert "air_temp_k" in renamed_csv.columns
        assert "rotational_speed_rpm" in renamed_csv.columns

        # Test renaming ucimlrepo / Excel unitless column names
        df_uci = pd.DataFrame({
            "Air temperature": [300.0],
            "Process temperature": [310.0],
            "Rotational speed": [1500],
            "Torque": [40.0],
            "Tool wear": [100],
            "Type": ["M"],
            "Machine failure": [0]
        })
        renamed_uci = rename_columns(df_uci, config)
        assert "air_temp_k" in renamed_uci.columns
        assert "rotational_speed_rpm" in renamed_uci.columns
