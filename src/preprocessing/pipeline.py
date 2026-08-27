"""
Preprocessing Pipeline Module
==============================
End-to-end data preprocessing pipeline for the AI4I 2020 dataset.

Pipeline stages:
1. Column selection & renaming
2. Drop leakage columns (individual failure modes)
3. Drop ID columns
4. Encode categorical variables
5. Feature engineering
6. Train/Validation/Test split (stratified)
7. Scaling (fit on train only)
8. Class imbalance handling (on train only)

CRITICAL: All fitting operations use training data only to prevent data leakage.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

logger = logging.getLogger(__name__)


def drop_leakage_columns(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> pd.DataFrame:
    """Remove columns that leak the target variable.

    The individual failure mode columns (TWF, HDF, PWF, OSF, RNF)
    collectively determine 'Machine failure'. Including them would
    give the model direct access to the answer.

    Args:
        df: DataFrame with all columns.
        config: Project configuration.

    Returns:
        DataFrame without leakage columns.
    """
    leakage_cols = config["data"]["leakage_columns"]
    cols_to_drop = [c for c in leakage_cols if c in df.columns]

    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        logger.info("Dropped leakage columns: %s", cols_to_drop)

    return df


def drop_id_columns(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> pd.DataFrame:
    """Remove non-predictive identifier columns.

    UDI and Product ID are identifiers, not features.

    Args:
        df: DataFrame.
        config: Project configuration.

    Returns:
        DataFrame without ID columns.
    """
    id_cols = config["data"]["id_columns"]
    cols_to_drop = [c for c in id_cols if c in df.columns]

    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        logger.info("Dropped ID columns: %s", cols_to_drop)

    return df


def encode_type_column(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> pd.DataFrame:
    """Encode the 'Type' column using ordinal encoding.

    L (Low quality) → 0
    M (Medium quality) → 1
    H (High quality) → 2

    This ordinal mapping preserves the quality hierarchy.

    Args:
        df: DataFrame.
        config: Project configuration.

    Returns:
        DataFrame with encoded Type column.
    """
    encoding = config["preprocessing"]["type_encoding"]
    col_name = "type" if "type" in df.columns else "Type"

    if col_name in df.columns:
        df[col_name] = df[col_name].map(encoding)
        if df[col_name].isnull().any():
            logger.warning("Unseen or null values found in '%s' column. Filling with 0.", col_name)
            df[col_name] = df[col_name].fillna(0)
        logger.info("Encoded '%s' column: %s", col_name, encoding)

    return df


def rename_columns(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> pd.DataFrame:
    """Rename columns to clean internal names.

    Args:
        df: DataFrame with raw column names.
        config: Project configuration.

    Returns:
        DataFrame with renamed columns.
    """
    rename_map = config["data"]["feature_names"]
    df = df.rename(columns=rename_map)
    return df


def split_data(
    df: pd.DataFrame,
    config: Dict[str, Any],
    target_col: str = "machine_failure",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame,
           pd.Series, pd.Series, pd.Series]:
    """Split data into train/validation/test sets with stratification.

    Split ratios: 70% train, 15% validation, 15% test.
    Stratification ensures class ratios are preserved in each split.

    Args:
        df: Preprocessed DataFrame (features + target).
        config: Project configuration.
        target_col: Target column name.

    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test).
    """
    seed = config["project"]["random_seed"]
    test_size = config["splitting"]["test_size"]
    val_size = config["splitting"]["val_size"]

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=seed,
        stratify=y if config["splitting"]["stratify"] else None,
    )

    # Second split: separate validation from training
    # Adjust val_size relative to remaining data
    val_fraction = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=val_fraction,
        random_state=seed,
        stratify=y_temp if config["splitting"]["stratify"] else None,
    )

    logger.info(
        "Data split — Train: %d (%.1f%%), Val: %d (%.1f%%), Test: %d (%.1f%%)",
        len(X_train), len(X_train) / len(df) * 100,
        len(X_val), len(X_val) / len(df) * 100,
        len(X_test), len(X_test) / len(df) * 100,
    )
    logger.info(
        "Class distribution — Train: %.2f%%, Val: %.2f%%, Test: %.2f%%",
        y_train.mean() * 100, y_val.mean() * 100, y_test.mean() * 100,
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def fit_scaler(
    X_train: pd.DataFrame,
    config: Dict[str, Any],
    feature_cols: list = None,
) -> Any:
    """Fit a scaler on training data only.

    Args:
        X_train: Training features.
        config: Project configuration.
        feature_cols: Columns to scale (numerical only).

    Returns:
        Fitted scaler object.
    """
    method = config["preprocessing"]["scaling_method"]

    if method == "standard":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    elif method == "robust":
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unknown scaling method: {method}")

    if feature_cols is None:
        feature_cols = config["preprocessing"]["numerical_features"]

    # Only scale columns that exist
    cols_to_scale = [c for c in feature_cols if c in X_train.columns]
    scaler.fit(X_train[cols_to_scale])

    logger.info("Fitted %s scaler on %d columns.", method, len(cols_to_scale))
    return scaler


def apply_scaler(
    X: pd.DataFrame,
    scaler: Any,
    config: Dict[str, Any],
    feature_cols: list = None,
) -> pd.DataFrame:
    """Apply a fitted scaler to a DataFrame.

    Args:
        X: Feature DataFrame.
        scaler: Fitted scaler object.
        config: Project configuration.
        feature_cols: Columns to scale.

    Returns:
        Scaled DataFrame.
    """
    X = X.copy()

    if feature_cols is None:
        feature_cols = config["preprocessing"]["numerical_features"]

    cols_to_scale = [c for c in feature_cols if c in X.columns]
    X[cols_to_scale] = scaler.transform(X[cols_to_scale])

    return X


def handle_class_imbalance(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: Dict[str, Any],
) -> Tuple[pd.DataFrame, pd.Series]:
    """Handle class imbalance in training data.

    Strategy is configurable:
    - 'class_weight': No resampling (handled by model's class_weight parameter)
    - 'smote': Apply SMOTE oversampling to minority class
    - 'none': No imbalance handling

    CRITICAL: Only applied to training data. Never to validation/test.

    Args:
        X_train: Training features.
        y_train: Training labels.
        config: Project configuration.

    Returns:
        Tuple of (resampled X_train, resampled y_train).
    """
    strategy = config["imbalance"]["strategy"]

    if strategy == "smote":
        from imblearn.over_sampling import SMOTE

        smote_config = config["imbalance"]["smote"]
        smote = SMOTE(
            sampling_strategy=smote_config["sampling_strategy"],
            k_neighbors=smote_config["k_neighbors"],
            random_state=config["project"]["random_seed"],
        )

        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

        logger.info(
            "SMOTE applied — Before: %d samples (%.1f%% positive), "
            "After: %d samples (%.1f%% positive)",
            len(y_train), y_train.mean() * 100,
            len(y_resampled), y_resampled.mean() * 100,
        )

        return pd.DataFrame(X_resampled, columns=X_train.columns), pd.Series(y_resampled, name=y_train.name)

    elif strategy == "class_weight":
        logger.info(
            "Class imbalance handled via model class_weight parameter. "
            "No resampling applied."
        )
        return X_train, y_train

    elif strategy == "none":
        logger.info("No class imbalance handling applied.")
        return X_train, y_train

    else:
        raise ValueError(f"Unknown imbalance strategy: {strategy}")


def run_preprocessing_pipeline(
    df: pd.DataFrame,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute the complete preprocessing pipeline.

    Pipeline steps:
    1. Drop leakage columns
    2. Drop ID columns
    3. Rename columns
    4. Encode categorical variables
    5. Feature engineering
    6. Train/Val/Test split
    7. Scale features (fit on train)
    8. Handle class imbalance (train only)

    Args:
        df: Raw DataFrame.
        config: Project configuration.

    Returns:
        Dictionary with all processed data and fitted transformers.
    """
    from src.features.engineer import engineer_features, get_all_feature_names

    logger.info("=" * 60)
    logger.info("Starting preprocessing pipeline")
    logger.info("=" * 60)

    # Step 1: Drop leakage columns
    df = drop_leakage_columns(df, config)

    # Step 2: Drop ID columns
    df = drop_id_columns(df, config)

    # Step 3: Rename columns
    df = rename_columns(df, config)

    # Step 4: Encode categorical
    df = encode_type_column(df, config)

    # Step 5: Split BEFORE feature engineering thresholds
    # (to prevent leakage from threshold computation)
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df, config)

    # Step 6: Feature engineering
    # Fit thresholds on training data only
    X_train, feat_stats = engineer_features(X_train, config, fit_stats=None)
    X_val, _ = engineer_features(X_val, config, fit_stats=feat_stats)
    X_test, _ = engineer_features(X_test, config, fit_stats=feat_stats)

    # Get final feature list
    feature_names = [c for c in X_train.columns]

    # Step 7: Scale numerical features
    # Determine which columns to scale (all numerical, including engineered)
    numerical_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    scaler = fit_scaler(X_train, config, feature_cols=numerical_cols)
    X_train_scaled = apply_scaler(X_train, scaler, config, feature_cols=numerical_cols)
    X_val_scaled = apply_scaler(X_val, scaler, config, feature_cols=numerical_cols)
    X_test_scaled = apply_scaler(X_test, scaler, config, feature_cols=numerical_cols)

    # Step 8: Handle class imbalance (training data only)
    X_train_balanced, y_train_balanced = handle_class_imbalance(
        X_train_scaled, y_train, config
    )

    logger.info("Preprocessing pipeline complete.")
    logger.info("Final feature count: %d", len(feature_names))
    logger.info("Training samples: %d", len(X_train_balanced))

    return {
        # Processed data
        "X_train": X_train_balanced,
        "X_val": X_val_scaled,
        "X_test": X_test_scaled,
        "y_train": y_train_balanced,
        "y_val": y_val,
        "y_test": y_test,
        # Unscaled data (for SHAP interpretability)
        "X_train_unscaled": X_train,
        "X_val_unscaled": X_val,
        "X_test_unscaled": X_test,
        # Fitted transformers
        "scaler": scaler,
        "feature_stats": feat_stats,
        "feature_names": feature_names,
        "numerical_cols": numerical_cols,
        # Original split (for ablation studies)
        "X_train_original": X_train,
        "y_train_original": y_train,
    }


def preprocess_single_input(
    input_data: Dict[str, float],
    config: Dict[str, Any],
    scaler: Any,
    feature_stats: Dict[str, float],
    feature_names: list,
    numerical_cols: list,
) -> pd.DataFrame:
    """Preprocess a single user input for prediction.

    Used by the dashboard when a user manually enters machine parameters.

    Args:
        input_data: Dictionary with raw feature values.
        config: Project configuration.
        scaler: Fitted scaler.
        feature_stats: Fitted feature engineering statistics.
        feature_names: Expected feature column order.
        numerical_cols: Columns to scale.

    Returns:
        Preprocessed DataFrame ready for model prediction.
    """
    from src.features.engineer import engineer_features

    # Create single-row DataFrame
    df = pd.DataFrame([input_data])

    # Feature engineering (using pre-computed stats)
    df, _ = engineer_features(df, config, fit_stats=feature_stats)

    # Ensure column order matches training
    missing_cols = set(feature_names) - set(df.columns)
    for col in missing_cols:
        df[col] = 0

    df = df[feature_names]

    # Scale
    cols_to_scale = [c for c in numerical_cols if c in df.columns]
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    return df
