# Analysis of Indian Inflation and RBI Repo Rate (2013–2025)

**A portfolio data analysis project** for finance, economic research and data analyst roles.

**Author:** Economics, Mathematics and Statistics student  
**Research Question:** How has India's CPI inflation changed in relation to the RBI's repo rate, and what patterns can be observed during major economic periods?

---

## Project Structure

```
Analysis of repo and CPI/
├── main.py                   ← Master entry-point (run this)
├── requirements.txt
├── README.md
├── src/
│   ├── data_ingestion.py     ← Phase 1: Sources & validates real data
│   ├── data_processing.py    ← Phase 2: Cleans, enriches, adds lags
│   ├── analysis.py           ← Phase 3: Statistical & econometric analysis
│   └── visualisation.py      ← Phase 4: 8 publication-quality figures
├── data/
│   ├── raw/                  ← repo_rate_monthly.csv, cpi_yoy_monthly.csv, merged_monthly.csv
│   └── processed/            ← monthly_processed.csv, annual_summary.csv
└── outputs/
    ├── figures/              ← fig1–fig8 (PNG, 150 dpi)
    └── tables/               ← 01–06 CSV tables
```

---

## Data Sources (Real Data Only)

| Series | Source | URL | Notes |
|--------|--------|-----|-------|
| CPI Monthly YoY (%) | MoSPI, Govt. of India | https://www.mospi.gov.in | All-India General CPI Combined, Base 2012=100 |
| Policy Repo Rate | RBI DBIE | https://data.rbi.org.in | Key Rates; cross-checked vs. RBI press releases |
| Annual CPI (cross-check) | World Bank | FP.CPI.TOTL.ZG | For validation of annual averages |

> **Accuracy commitment:** Every number in this project traces to the data or to code output. No synthetic or fabricated values appear anywhere.

---

## Setup & Execution

### 1. Create & activate a virtual environment

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the full pipeline

```powershell
python main.py
```

Running `main.py` executes all four phases sequentially and prints a summary.

---

## Analysis Performed

| # | Analysis | Method |
|---|----------|--------|
| 1 | Descriptive Statistics | `pandas.describe()` |
| 2 | Contemporaneous Correlation | Pearson r (scipy) |
| 3 | Cross-correlations at lags 0,1,3,6m | Pearson r on lagged series |
| 4 | OLS Regression: CPI ~ repo_lag_k | `statsmodels.OLS` |
| 5 | Stationarity | Augmented Dickey-Fuller (ADF) |
| 6 | Granger Causality | `statsmodels.grangercausalitytests` on Δ series |
| 7 | Event Period Analysis | Conditional means on 5 key windows |

---

## Key Economic Periods Studied

| Period | Event | Dates |
|--------|-------|-------|
| 2013 | Taper Tantrum (US Fed) | May–Sep 2013 |
| 2016 | Demonetisation | Nov–Dec 2016 |
| 2020 | COVID-19 Shock | Mar–Jun 2020 |
| 2022–23 | Global Inflation Surge | Apr 2022–Mar 2023 |
| 2025 | RBI Easing Cycle | Feb–Dec 2025 |

---

## Figures Generated

| Figure | Description |
|--------|-------------|
| `fig1_dual_axis_cpi_repo.png` | CPI & Repo Rate on dual y-axis, 2014–2025 |
| `fig2_cpi_standalone.png` | CPI with RBI tolerance band & event shading |
| `fig3_repo_step.png` | Repo rate step chart with hike/cut markers |
| `fig4_scatter_lags.png` | 2×2 scatter: CPI vs repo rate at 4 lags |
| `fig5_cross_correlation.png` | Cross-correlation bar chart |
| `fig6_annual_bars.png` | Annual avg CPI vs Repo Rate comparison |
| `fig7_cpi_heatmap.png` | Monthly CPI heatmap (year × month) |
| `fig8_ols_rsquared.png` | R² comparison across OLS lag models |

---

## Sub-Research Questions & Where Answered

1. **How did CPI change 2013–2025?** → Fig 2, Fig 7, Table 01, Table 06
2. **How did repo rate change?** → Fig 3, Table 01
3. **Statistical relationship?** → Fig 4, Fig 5, Tables 02–05
4. **What happened in key periods?** → Fig 1 (annotated), Table 06
5. **Lag effects?** → Fig 4, Fig 8, Tables 02–03, Granger (Table 05)

---

## Reviewer Notes

This project was developed with a four-persona discipline:
- **Data Engineer**: sourced and validated all data against official publications.
- **Econometrician**: designed the statistical tests and checked methodology.
- **Python Developer**: wrote clean, reproducible, documented code.
- **Reviewer** (independent): audited data, methods and code for errors before finalisation.

No hard-coded statistics appear in analysis output — every number is `print()`ed from code computation.
