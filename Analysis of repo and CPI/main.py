"""
main.py
=======
Entry-point for the project.
"Analysis of Indian Inflation and RBI Repo Rate: Trends, Relationships,
and Monetary Policy (2013-2025)"

Run this script to execute the full pipeline end-to-end:
    python main.py

Pipeline
--------
Phase 1  data_ingestion   → sources & saves raw data (data/raw/)
Phase 2  data_processing  → cleans, enriches, saves (data/processed/)
Phase 3  analysis         → statistical tests, saves tables (outputs/tables/)
Phase 4  visualisation    → 8 publication-quality charts (outputs/figures/)

All printed numbers are code-computed from verified data — no hard-coded
statistics appear in this project.
"""

import sys
import os
import time

# Ensure src is importable whether run from the project root or the src/ dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def banner(text: str):
    width = 70
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def main():
    t0 = time.time()

    banner("PHASE 1 — Data Ingestion")
    from src.data_ingestion import merge_and_save
    raw_df = merge_and_save()

    banner("PHASE 2 — Data Processing")
    from src.data_processing import run_processing
    df, annual_df = run_processing()

    banner("PHASE 3 — Statistical Analysis")
    from src.analysis import run_analysis
    results = run_analysis(df)

    banner("PHASE 4 — Visualisation")
    from src.visualisation import generate_all_figures
    generate_all_figures(df, annual_df, results)

    elapsed = time.time() - t0
    banner(f"PIPELINE COMPLETE  ({elapsed:.1f}s)")
    print()
    print("  Outputs")
    print("  -------")
    print("  data/raw/          → repo_rate_monthly.csv, cpi_yoy_monthly.csv, merged_monthly.csv")
    print("  data/processed/    → monthly_processed.csv, annual_summary.csv")
    print("  outputs/tables/    → 01_descriptive_stats.csv … 06_event_analysis.csv")
    print("  outputs/figures/   → fig1_dual_axis_cpi_repo.png … fig8_ols_rsquared.png")
    print()
    print("  Research Question Summary")
    print("  -------------------------")
    ann = results["annual_summary"]
    xcorr = results["cross_correlations"]
    gc    = results["granger"]

    print(f"  • CPI range (2014–2025):  {ann['cpi_min'].min():.2f}% – {ann['cpi_max'].max():.2f}%")
    print(f"  • Repo rate range        :  {df['repo_rate'].min():.2f}% – {df['repo_rate'].max():.2f}%")
    print(f"  • Pearson r (contemp.)   :  {results['pearson_r']:+.4f} (p={results['pearson_p']:.4f})")
    best_xcorr = xcorr.loc[xcorr["pearson_r"].abs().idxmax()]
    print(f"  • Strongest cross-corr.  :  r={best_xcorr['pearson_r']:+.4f} at lag {int(best_xcorr['lag_months'])}m")
    gc_sig = gc[gc["reject_H0_5pct"]]
    if len(gc_sig):
        print(f"  • Granger causality      :  Significant at lag(s): {list(gc_sig['lag'].values)} months")
    else:
        print(f"  • Granger causality      :  No significant lag found at 5% level")


if __name__ == "__main__":
    main()
