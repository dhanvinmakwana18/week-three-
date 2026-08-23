"""
Data loading module for the Wine Quality statistical analysis project.
Downloads and caches the UCI Wine Quality dataset.
"""

from pathlib import Path
import urllib.request
import urllib.error
import pandas as pd

UCI_RED_WINE_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
)
FALLBACK_RED_WINE_URL = (
    "https://raw.githubusercontent.com/anndvision/wine-quality/master/winequality-red.csv"
)

EXPECTED_COLUMNS = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "quality",
]


def download_dataset(target_path: Path, url: str = UCI_RED_WINE_URL) -> None:
    """
    Download the dataset from a remote URL to the specified local path.

    Parameters
    ----------
    target_path : Path
        Local file path where the raw CSV will be saved.
    url : str
        Remote URL of the dataset.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        with open(target_path, "wb") as f:
            f.write(data)
    except (urllib.error.URLError, TimeoutError) as primary_error:
        req = urllib.request.Request(FALLBACK_RED_WINE_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        with open(target_path, "wb") as f:
            f.write(data)


def load_raw_data(data_dir: Path, force_download: bool = False) -> pd.DataFrame:
    """
    Load raw wine quality dataset, downloading if necessary.

    Parameters
    ----------
    data_dir : Path
        Path to the project data directory containing 'raw/'.
    force_download : bool, default=False
        If True, re-download the dataset even if local file exists.

    Returns
    -------
    pd.DataFrame
        Raw wine quality dataset.
    """
    raw_file_path = data_dir / "raw" / "winequality-red.csv"

    if force_download or not raw_file_path.exists():
        download_dataset(raw_file_path)

    df = pd.read_csv(raw_file_path, sep=";")

    # Validate delimiter fallback if parsed as single column
    if df.shape[1] == 1:
        df = pd.read_csv(raw_file_path, sep=",")

    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns in raw data: {missing_cols}")

    if len(df) == 0:
        raise ValueError("Loaded dataset contains 0 rows.")

    return df
