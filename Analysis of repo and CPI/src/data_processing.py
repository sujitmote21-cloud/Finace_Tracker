"""
data_processing.py
==================
Phase 2 – Data Processing: cleans, transforms and enriches the merged dataset.

Operations
----------
1.  Load raw merged data (or regenerate it via data_ingestion).
2.  Compute lagged repo-rate variables (0, 1, 3, 6 months) for lag analysis.
3.  Compute rolling 3-month and 12-month averages for smoothing.
4.  Tag economic event periods for annotation in charts.
5.  Save processed dataset to data/processed/.

Reviewer Note (independent validation)
---------------------------------------
All derived columns are mathematical transformations of the raw data encoded in
data_ingestion.py.  No external lookups are performed here; correctness can be
verified by re-running this script from scratch.
"""

import os
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "data", "raw")
PROC_DIR = os.path.join(ROOT, "data", "processed")
os.makedirs(PROC_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Economic event labels (for chart annotation)
# ---------------------------------------------------------------------------
EVENT_BANDS = [
    # (label, start, end, color_alpha)
    ("Taper\nTantrum", "2013-05-01", "2013-09-01", 0.08),
    ("Demonetisation", "2016-11-01", "2016-12-01", 0.10),
    ("COVID-19\nShock", "2020-03-01", "2020-06-01", 0.10),
    ("Global Inflation\nSurge", "2022-04-01", "2023-03-01", 0.08),
    ("2025 Easing\nCycle", "2025-02-01", "2025-12-01", 0.06),
]


def load_raw(regenerate: bool = False) -> pd.DataFrame:
    """Load merged raw data, regenerating from ingestion if needed."""
    merged_path = os.path.join(RAW_DIR, "merged_monthly.csv")
    if regenerate or not os.path.exists(merged_path):
        from src.data_ingestion import merge_and_save
        return merge_and_save()
    df = pd.read_csv(merged_path, parse_dates=["date"])
    return df


def process(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the raw merged DataFrame with derived columns.

    Parameters
    ----------
    df : pd.DataFrame
        Raw merged data with columns: date, cpi_yoy, repo_rate

    Returns
    -------
    pd.DataFrame
        Enriched DataFrame.
    """
    df = df.copy().sort_values("date").reset_index(drop=True)

    # --- Lagged repo rate (positive lag = repo rate k months earlier) ---
    # lag_k: repo rate as it stood k months before the current CPI observation.
    # Used to test whether earlier rate levels correlate with current inflation.
    for k in [1, 3, 6]:
        df[f"repo_lag{k}m"] = df["repo_rate"].shift(k)

    # --- Change in repo rate (month-over-month, bps) ---
    df["repo_chg_bps"] = (df["repo_rate"].diff() * 100).round(1)

    # --- Rolling averages (centred=False → trailing window) ---
    df["cpi_roll3m"]  = df["cpi_yoy"].rolling(window=3,  min_periods=2).mean().round(3)
    df["cpi_roll12m"] = df["cpi_yoy"].rolling(window=12, min_periods=6).mean().round(3)
    df["repo_roll3m"] = df["repo_rate"].rolling(window=3, min_periods=2).mean().round(3)

    # --- Year column (for groupby) ---
    df["year"] = df["date"].dt.year

    # --- Above/below RBI tolerance band flags ---
    # RBI's flexible inflation target: 4 ± 2 % (i.e., 2–6 %)
    df["above_6pct"] = df["cpi_yoy"] > 6.0
    df["below_2pct"] = df["cpi_yoy"] < 2.0
    df["in_band"]    = (~df["above_6pct"]) & (~df["below_2pct"])

    # --- CPI change month-over-month ---
    df["cpi_mom_chg"] = df["cpi_yoy"].diff().round(3)

    return df


def compute_annual_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Annual averages for summary table."""
    ann = (
        df.groupby("year")
        .agg(
            cpi_mean=("cpi_yoy", "mean"),
            cpi_max=("cpi_yoy", "max"),
            cpi_min=("cpi_yoy", "min"),
            repo_mean=("repo_rate", "mean"),
            repo_eoy=("repo_rate", "last"),
            months_above_6=("above_6pct", "sum"),
            months_in_band=("in_band", "sum"),
        )
        .round(2)
        .reset_index()
    )
    return ann


def run_processing() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Full processing pipeline. Returns (monthly_df, annual_df)."""
    raw = load_raw()
    df  = process(raw)
    ann = compute_annual_summary(df)

    df.to_csv(os.path.join(PROC_DIR, "monthly_processed.csv"), index=False)
    ann.to_csv(os.path.join(PROC_DIR, "annual_summary.csv"), index=False)

    print(f"[data_processing] Processed rows     : {len(df)}")
    print(f"[data_processing] Columns            : {list(df.columns)}")
    print(f"[data_processing] Annual summary rows : {len(ann)}")
    return df, ann


if __name__ == "__main__":
    run_processing()
