"""
Data Loader Module
==================
Handles downloading and loading the AI4I 2020 Predictive Maintenance Dataset.

Dataset: AI4I 2020 Predictive Maintenance Dataset
Official UCI ID: 601
Source: https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
Size: 10,000 records, 14 columns
"""

import os
import logging
import zipfile
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
import yaml

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Load project configuration from YAML file.

    Args:
        config_path: Path to config.yaml file.

    Returns:
        Configuration dictionary.

    Raises:
        FileNotFoundError: If config file does not exist.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        # Try relative to project root
        project_root = Path(__file__).resolve().parent.parent.parent
        config_file = project_root / config_path

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logger.info("Configuration loaded from %s", config_file)
    return config


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path to project root (parent of src/).
    """
    return Path(__file__).resolve().parent.parent.parent


def fetch_dataset_ucirepo(uci_id: int = 601) -> pd.DataFrame:
    """Fetch the dataset directly using the ucimlrepo package.

    Usage:
        from ucimlrepo import fetch_ucirepo
        ai4i = fetch_ucirepo(id=601)
        X = ai4i.data.features
        y = ai4i.data.targets

    Args:
        uci_id: UCI dataset repository ID (601 for AI4I 2020).

    Returns:
        Combined pandas DataFrame with original dataset structure.
    """
    try:
        from ucimlrepo import fetch_ucirepo
        logger.info("Fetching dataset from ucimlrepo (id=%d)...", uci_id)
        dataset = fetch_ucirepo(id=uci_id)
        
        # Use full original dataframe if available
        if hasattr(dataset.data, "original") and dataset.data.original is not None:
            df = dataset.data.original.copy()
        else:
            X = dataset.data.features
            y = dataset.data.targets
            df = pd.concat([X, y], axis=1)

        logger.info("ucimlrepo fetch successful: %d rows, %d columns", len(df), len(df.columns))
        return df
    except Exception as e:
        logger.warning("ucimlrepo fetch failed: %s", e)
        raise


def download_dataset(config: Dict[str, Any]) -> Path:
    """Download or locate the AI4I 2020 dataset locally.

    Checks:
    1. Standard CSV path in data/raw/
    2. Excel files (.xlsx, .xls) in data/raw/ or project root
    3. Alternate CSV filenames
    4. Downloads via ZIP or ucimlrepo if not present locally

    Args:
        config: Project configuration dictionary.

    Returns:
        Path to the local dataset file (CSV or Excel).
    """
    project_root = get_project_root()
    raw_dir = project_root / config["data"]["raw_dir"]
    raw_dir.mkdir(parents=True, exist_ok=True)

    csv_path = raw_dir / config["data"]["dataset_filename"]

    # Check if dataset already exists as CSV
    if csv_path.exists():
        logger.info("Dataset already exists at %s", csv_path)
        return csv_path

    # Check for Excel files in raw_dir or project root
    for search_dir in [raw_dir, project_root]:
        for ext in ["*.xlsx", "*.xls"]:
            excel_files = list(search_dir.glob(ext))
            if excel_files:
                logger.info("Found Excel dataset at %s", excel_files[0])
                return excel_files[0]

    # Check for common alternate CSV filenames
    for alt_name in ["ai4i2020.csv", "ai4i_2020.csv", "predictive_maintenance.csv"]:
        for search_dir in [raw_dir, project_root]:
            alt_path = search_dir / alt_name
            if alt_path.exists():
                logger.info("Found dataset at %s", alt_path)
                return alt_path

    # Try ucimlrepo fetch first
    try:
        df_uci = fetch_dataset_ucirepo(uci_id=601)
        df_uci.to_csv(csv_path, index=False)
        logger.info("Saved ucimlrepo dataset to %s", csv_path)
        return csv_path
    except Exception as e:
        logger.info("ucimlrepo fetch fallback: downloading ZIP directly...")

    # Download ZIP fallback from UCI
    url = config["data"]["dataset_url"]
    zip_path = raw_dir / "dataset.zip"

    logger.info("Downloading AI4I 2020 dataset from %s", url)
    try:
        urllib.request.urlretrieve(url, zip_path)
        logger.info("Download complete. Extracting...")

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(raw_dir)

        csv_files = list(raw_dir.glob("*.csv"))
        if csv_files:
            found_csv = csv_files[0]
            if found_csv.name != config["data"]["dataset_filename"]:
                found_csv.rename(csv_path)
            logger.info("Dataset extracted to %s", csv_path)
        else:
            raise FileNotFoundError("No CSV file found in downloaded archive.")

        if zip_path.exists():
            zip_path.unlink()

    except Exception as e:
        logger.error("Failed to download dataset: %s", e)
        logger.info("Place CSV/Excel file at: %s", csv_path)
        raise

    return csv_path



def load_from_database(db_type: str, connection_string: str, query_or_table: str) -> pd.DataFrame:
    """Load dataset directly from an external database (PostgreSQL, MySQL, SQLite, MongoDB, Snowflake)."""
    try:
        import sqlalchemy
        engine = sqlalchemy.create_engine(connection_string)
        if query_or_table.strip().lower().startswith("select"):
            df = pd.read_sql_query(query_or_table, engine)
        else:
            df = pd.read_sql_table(query_or_table, engine)
        return df
    except Exception as e:
        logger.error("Failed to fetch data from database (%s): %s", db_type, e)
        raise RuntimeError(f"Database Connection Error ({db_type}): {e}")

def load_dataset(
    config: Dict[str, Any],
    filepath: Optional[str] = None
) -> pd.DataFrame:
    """Load the AI4I 2020 dataset into a pandas DataFrame.

    Supports reading CSV (.csv) and Excel (.xlsx, .xls) files.

    Args:
        config: Project configuration dictionary.
        filepath: Optional explicit path to CSV or Excel file.

    Returns:
        Raw DataFrame with all columns.

    Raises:
        FileNotFoundError: If dataset file cannot be found.
        ValueError: If loaded DataFrame is empty.
    """
    if filepath:
        file_path = Path(filepath)
    else:
        file_path = download_dataset(config)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at {file_path}")

    logger.info("Loading dataset from %s", file_path)

    # Auto-detect file format
    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("Loaded dataset is empty.")

    logger.info("Dataset loaded: %d rows, %d columns", len(df), len(df.columns))
    logger.info("Columns: %s", list(df.columns))

    return df


def rename_columns(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> pd.DataFrame:
    """Rename dataset columns to clean internal names.

    Args:
        df: Raw DataFrame.
        config: Project configuration.

    Returns:
        DataFrame with renamed columns.
    """
    rename_map = config["data"]["feature_names"]
    df_renamed = df.rename(columns=rename_map)
    logger.info("Columns renamed: %s", list(rename_map.keys()))
    return df_renamed


def get_dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate a comprehensive summary of the dataset.

    Args:
        df: Loaded DataFrame.

    Returns:
        Dictionary containing dataset metadata and statistics.
    """
    summary = {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "total_missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        "numerical_stats": {},
        "categorical_stats": {},
    }

    numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numerical_cols:
        summary["numerical_stats"][col] = {
            "mean": round(float(df[col].mean()), 4),
            "std": round(float(df[col].std()), 4),
            "min": round(float(df[col].min()), 4),
            "max": round(float(df[col].max()), 4),
            "median": round(float(df[col].median()), 4),
            "q25": round(float(df[col].quantile(0.25)), 4),
            "q75": round(float(df[col].quantile(0.75)), 4),
        }

    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        summary["categorical_stats"][col] = df[col].value_counts().to_dict()

    logger.info(
        "Dataset summary: %d rows, %d cols, %d missing, %d duplicates",
        summary["n_rows"], summary["n_columns"],
        summary["total_missing"], summary["duplicates"]
    )

    return summary
