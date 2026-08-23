"""
Data cleaning and preparation module for the Wine Quality dataset.
Handles column renaming, type validation, missing value inspection,
outlier detection, and analytical categorical grouping.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def clean_and_prepare_data(
    raw_df: pd.DataFrame, output_dir: Path
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Clean, validate, and prepare the raw wine quality dataset.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Raw dataset loaded from the repository.
    output_dir : Path
        Path to the data directory where processed files are stored.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, Any]]
        Cleaned dataframe with derived analytical columns and a summary dictionary.
    """
    df = raw_df.copy()

    # Standardize column headers to snake_case
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Data shape and missing values check
    initial_rows = len(df)
    missing_counts = df.isnull().sum().to_dict()
    total_missing = sum(missing_counts.values())

    # Data type conversion and verification
    numeric_columns = [
        "fixed_acidity",
        "volatile_acidity",
        "citric_acid",
        "residual_sugar",
        "chlorides",
        "free_sulfur_dioxide",
        "total_sulfur_dioxide",
        "density",
        "ph",
        "sulphates",
        "alcohol",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["quality"] = df["quality"].astype(int)

    # Duplicate records inspection
    duplicate_count = int(df.duplicated().sum())

    # Outlier detection on alcohol using IQR method
    q1 = df["alcohol"].quantile(0.25)
    q3 = df["alcohol"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    alcohol_outliers = int(((df["alcohol"] < lower_bound) | (df["alcohol"] > upper_bound)).sum())

    # Analytical categorizations
    # Quality Tier: Low (3-5), Medium (6), High (7-8)
    def assign_quality_tier(q: int) -> str:
        if q <= 5:
            return "Low (3-5)"
        elif q == 6:
            return "Medium (6)"
        else:
            return "High (7-8)"

    df["quality_tier"] = df["quality"].apply(assign_quality_tier)

    # Binary Quality Comparison for Secondary Hypothesis: Low (<=5) vs High (>=7)
    def assign_binary_quality(q: int) -> str:
        if q <= 5:
            return "Low (<=5)"
        elif q >= 7:
            return "High (>=7)"
        return "Medium (6)"

    df["binary_quality"] = df["quality"].apply(assign_binary_quality)

    # Save cleaned processed dataset
    processed_dir = output_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_file_path = processed_dir / "winequality_cleaned.csv"
    df.to_csv(processed_file_path, index=False)

    summary = {
        "initial_rows": initial_rows,
        "final_rows": len(df),
        "total_columns": len(df.columns),
        "total_missing": total_missing,
        "duplicate_rows": duplicate_count,
        "alcohol_q1": float(q1),
        "alcohol_q3": float(q3),
        "alcohol_iqr": float(iqr),
        "alcohol_lower_bound": float(lower_bound),
        "alcohol_upper_bound": float(upper_bound),
        "alcohol_outliers_count": alcohol_outliers,
        "quality_counts": df["quality"].value_counts().sort_index().to_dict(),
        "quality_tier_counts": df["quality_tier"].value_counts().to_dict(),
    }

    return df, summary
