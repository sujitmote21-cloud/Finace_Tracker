"""
visualisation.py
================
Phase 4 – Publication-quality charts for the portfolio project.

Figures produced
----------------
Fig 1:  Dual-axis time-series: CPI YoY (%) & Repo Rate (%) 2014–2025
Fig 2:  CPI YoY standalone with RBI tolerance band and event annotations
Fig 3:  Repo rate step-chart with policy action markers
Fig 4:  Scatter plots (4-panel): CPI vs repo_lag_k for k = 0,1,3,6 months
Fig 5:  Cross-correlation bar chart (lags 0–6)
Fig 6:  Annual average bar chart (CPI vs Repo Rate side-by-side)
Fig 7:  Heatmap: monthly CPI YoY (year × month)
Fig 8:  OLS R² across lag models (bar)

All figures saved as high-res PNG to outputs/figures/.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")
matplotlib.rcParams["figure.dpi"] = 150

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(ROOT, "outputs", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
PALETTE = {
    "cpi": "#E63946",          # vibrant red
    "repo": "#457B9D",         # steel blue
    "band_fill": "#A8DADC",    # light teal for RBI band
    "event": "#F4A261",        # orange for event bands
    "neutral": "#2B2D42",      # dark charcoal
    "bg": "#F8F9FA",           # off-white background
    "grid": "#DEE2E6",         # subtle grid
    "positive": "#2DC653",     # green
    "negative": "#E63946",     # red
}

EVENT_BANDS = [
    ("Taper Tantrum\n(May–Sep 2013)", "2013-05-01", "2013-09-30", "#F4A261"),
    ("Demonetisation\n(Nov–Dec 2016)", "2016-11-01", "2016-12-31", "#9B5DE5"),
    ("COVID-19 Shock\n(Mar–Jun 2020)", "2020-03-01", "2020-06-30", "#E63946"),
    ("Global Inflation\nSurge (Apr 2022–Mar 2023)", "2022-04-01", "2023-03-31", "#F4A261"),
    ("2025 Easing Cycle\n(Feb–Dec 2025)", "2025-02-01", "2025-12-31", "#2DC653"),
]


def _style_ax(ax, xlabel="", ylabel="", title=""):
    ax.set_facecolor(PALETTE["bg"])
    ax.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.5, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel(xlabel, fontsize=10, color=PALETTE["neutral"])
    ax.set_ylabel(ylabel, fontsize=10, color=PALETTE["neutral"])
    ax.set_title(title, fontsize=13, fontweight="bold", color=PALETTE["neutral"], pad=10)
    ax.tick_params(labelsize=9, colors=PALETTE["neutral"])


def _add_event_bands(ax, df: pd.DataFrame, alpha: float = 0.12):
    """Shade event periods on a time-series axis."""
    for label, start, end, color in EVENT_BANDS:
        s = pd.Timestamp(start)
        e = pd.Timestamp(end)
        # Only shade if within data range
        if e >= df["date"].min() and s <= df["date"].max():
            ax.axvspan(s, e, alpha=alpha, color=color, zorder=0)


def _save(fig, name: str):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 1: Dual-axis time-series
# ---------------------------------------------------------------------------
def fig1_dual_axis(df: pd.DataFrame):
    fig, ax1 = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("white")

    _add_event_bands(ax1, df)

    # CPI
    ax1.fill_between(df["date"], df["cpi_yoy"], alpha=0.18, color=PALETTE["cpi"])
    ax1.plot(df["date"], df["cpi_yoy"], color=PALETTE["cpi"], linewidth=2.0,
             label="CPI Inflation YoY (%)", zorder=3)
    # RBI tolerance band
    ax1.axhline(6.0, color=PALETTE["cpi"], linestyle=":", linewidth=1.0, alpha=0.5)
    ax1.axhline(2.0, color=PALETTE["repo"], linestyle=":", linewidth=1.0, alpha=0.5)
    ax1.axhline(4.0, color=PALETTE["neutral"], linestyle="--", linewidth=0.8, alpha=0.4)

    _style_ax(ax1, ylabel="CPI Inflation YoY (%)", title="India CPI Inflation vs RBI Policy Repo Rate (2014–2025)")
    ax1.yaxis.label.set_color(PALETTE["cpi"])
    ax1.tick_params(axis="y", colors=PALETTE["cpi"])
    ax1.set_ylim(-0.5, 12)

    # Repo rate on secondary axis
    ax2 = ax1.twinx()
    ax2.step(df["date"], df["repo_rate"], color=PALETTE["repo"], linewidth=2.2,
             where="post", label="RBI Repo Rate (%)", zorder=4)
    ax2.set_ylabel("RBI Policy Repo Rate (%)", fontsize=10, color=PALETTE["repo"])
    ax2.tick_params(axis="y", colors=PALETTE["repo"])
    ax2.yaxis.label.set_color(PALETTE["repo"])
    ax2.set_ylim(2.5, 10.5)
    ax2.spines[["top", "left"]].set_visible(False)

    # Date formatting
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 7, 10]))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=0, ha="center")

    # Combined legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    band_patch = mpatches.Patch(color=PALETTE["cpi"], alpha=0.2, label="RBI Tolerance Band (2–6%)")
    ax1.legend(h1 + h2 + [band_patch], l1 + l2 + ["RBI Tolerance Band (2–6%)"],
               loc="upper right", fontsize=9, framealpha=0.85)

    ax1.annotate("Data: MoSPI (CPI) | RBI DBIE (Repo Rate)",
                 xy=(0.01, 0.01), xycoords="axes fraction", fontsize=7.5,
                 color="gray", style="italic")

    _save(fig, "fig1_dual_axis_cpi_repo.png")


# ---------------------------------------------------------------------------
# Figure 2: CPI standalone with tolerance band & annotations
# ---------------------------------------------------------------------------
def fig2_cpi_standalone(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 5.5))
    fig.patch.set_facecolor("white")

    # Tolerance band fill
    ax.fill_between(df["date"], 2, 6, alpha=0.12, color=PALETTE["band_fill"],
                    label="RBI Target Band (2–6%)")
    _add_event_bands(ax, df, alpha=0.10)

    ax.plot(df["date"], df["cpi_yoy"], color=PALETTE["cpi"], linewidth=2.0,
            label="CPI Inflation YoY (%)", zorder=3)
    ax.plot(df["date"], df["cpi_roll12m"], color=PALETTE["neutral"], linewidth=1.4,
            linestyle="--", alpha=0.7, label="12-month Rolling Mean", zorder=3)
    ax.axhline(4.0, color=PALETTE["neutral"], linestyle="--", linewidth=0.8, alpha=0.5,
               label="RBI Target (4%)")
    ax.axhline(6.0, color=PALETTE["cpi"], linestyle=":", linewidth=0.9, alpha=0.6)
    ax.axhline(2.0, color=PALETTE["repo"], linestyle=":", linewidth=0.9, alpha=0.6)

    # Annotate peak moments
    peak_row = df.loc[df["cpi_yoy"].idxmax()]
    ax.annotate(f"Peak: {peak_row['cpi_yoy']:.2f}%\n({peak_row['date'].strftime('%b %Y')})",
                xy=(peak_row["date"], peak_row["cpi_yoy"]),
                xytext=(20, 8), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color=PALETTE["cpi"], lw=1.2),
                fontsize=8.5, color=PALETTE["cpi"], fontweight="bold")

    _style_ax(ax, xlabel="", ylabel="CPI Inflation YoY (%)",
              title="India CPI Inflation (YoY %) with RBI Tolerance Band — 2014–2025")
    ax.set_ylim(-0.5, 11)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper right", fontsize=9, framealpha=0.85)

    ax.annotate("Data: MoSPI All-India General CPI Combined (Base: 2012=100)",
                xy=(0.01, 0.01), xycoords="axes fraction", fontsize=7.5,
                color="gray", style="italic")
    _save(fig, "fig2_cpi_standalone.png")


# ---------------------------------------------------------------------------
# Figure 3: Repo Rate step chart
# ---------------------------------------------------------------------------
def fig3_repo_step(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 4.5))
    fig.patch.set_facecolor("white")
    _add_event_bands(ax, df, alpha=0.10)

    ax.step(df["date"], df["repo_rate"], color=PALETTE["repo"], linewidth=2.2,
            where="post", label="Policy Repo Rate", zorder=3)
    ax.fill_between(df["date"], df["repo_rate"], 3.5, step="post",
                    alpha=0.15, color=PALETTE["repo"])

    # Mark rate change months
    changes = df[df["repo_chg_bps"] != 0].copy()
    hike = changes[changes["repo_chg_bps"] > 0]
    cut  = changes[changes["repo_chg_bps"] < 0]
    ax.scatter(hike["date"], hike["repo_rate"], color="#E63946", s=55, zorder=5,
               label="Rate Hike", marker="^")
    ax.scatter(cut["date"],  cut["repo_rate"],  color="#2DC653", s=55, zorder=5,
               label="Rate Cut", marker="v")

    _style_ax(ax, ylabel="Repo Rate (% p.a.)",
              title="RBI Policy Repo Rate — History of Changes (2014–2025)")
    ax.set_ylim(3.5, 9)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper right", fontsize=9, framealpha=0.85)

    ax.annotate("Data: RBI DBIE — Key Rates (Policy Repo Rate)",
                xy=(0.01, 0.01), xycoords="axes fraction", fontsize=7.5,
                color="gray", style="italic")
    _save(fig, "fig3_repo_step.png")


# ---------------------------------------------------------------------------
# Figure 4: Scatter plots — CPI vs Repo Rate at 4 lags (2×2 panel)
# ---------------------------------------------------------------------------
def fig4_scatter_lags(df: pd.DataFrame):
    lag_cfg = [
        (0,  "repo_rate",  "Lag 0 (Contemporaneous)"),
        (1,  "repo_lag1m", "Lag 1 Month"),
        (3,  "repo_lag3m", "Lag 3 Months"),
        (6,  "repo_lag6m", "Lag 6 Months"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.patch.set_facecolor("white")
    fig.suptitle("CPI Inflation vs Lagged Repo Rate — Scatter Plots\n"
                 "India 2014–2025 (Monthly Data)", fontsize=14, fontweight="bold",
                 color=PALETTE["neutral"], y=1.01)

    for ax, (lag, col, title) in zip(axes.flat, lag_cfg):
        sub = df[["cpi_yoy", col, "year"]].dropna()
        # Color by year for temporal context
        sc = ax.scatter(sub[col], sub["cpi_yoy"],
                        c=sub["year"], cmap="viridis", s=40, alpha=0.75,
                        edgecolors="white", linewidths=0.4, zorder=3)
        # OLS line
        slope, intercept, r, p, _ = stats.linregress(sub[col], sub["cpi_yoy"])
        x_fit = np.linspace(sub[col].min(), sub[col].max(), 100)
        ax.plot(x_fit, intercept + slope * x_fit, color=PALETTE["cpi"],
                linewidth=1.8, linestyle="--", label=f"OLS fit", zorder=4)

        _style_ax(ax, xlabel=f"Repo Rate — {title} (%)",
                  ylabel="CPI Inflation YoY (%)", title=title)
        ax.text(0.05, 0.92, f"r = {r:+.3f}  (p={p:.3f})\nβ = {slope:+.3f}",
                transform=ax.transAxes, fontsize=8.5, color=PALETTE["neutral"],
                verticalalignment="top",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    # Shared colorbar
    cbar = fig.colorbar(sc, ax=axes, shrink=0.6, pad=0.02)
    cbar.set_label("Year", fontsize=10, color=PALETTE["neutral"])
    cbar.ax.tick_params(labelsize=8)

    fig.tight_layout()
    _save(fig, "fig4_scatter_lags.png")


# ---------------------------------------------------------------------------
# Figure 5: Cross-correlation bar chart
# ---------------------------------------------------------------------------
def fig5_crosscorr(results: dict):
    xcorr = results["cross_correlations"]
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("white")

    colors = [PALETTE["positive"] if r > 0 else PALETTE["negative"]
              for r in xcorr["pearson_r"]]
    bars = ax.bar(xcorr["lag_months"].astype(str) + "m",
                  xcorr["pearson_r"], color=colors, width=0.5, alpha=0.85,
                  edgecolor="white", linewidth=0.8)
    ax.axhline(0, color=PALETTE["neutral"], linewidth=0.8)

    # Significance asterisks
    for bar, (_, row) in zip(bars, xcorr.iterrows()):
        if row["significant_5pct"]:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + (0.01 if bar.get_height() >= 0 else -0.03),
                    "★", ha="center", va="bottom", fontsize=11, color=PALETTE["neutral"])

    _style_ax(ax, xlabel="Lag (months)", ylabel="Pearson r",
              title="Cross-Correlation: Repo Rate → CPI Inflation\n(★ = significant at 5%)")
    ax.set_ylim(-0.6, 0.6)
    ax.annotate("Positive r: higher repo rate associated with higher CPI at that lag.",
                xy=(0.01, 0.01), xycoords="axes fraction", fontsize=8, color="gray",
                style="italic")
    _save(fig, "fig5_cross_correlation.png")


# ---------------------------------------------------------------------------
# Figure 6: Annual average bar chart
# ---------------------------------------------------------------------------
def fig6_annual_bars(annual_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor("white")

    x = np.arange(len(annual_df))
    w = 0.38
    bars1 = ax.bar(x - w/2, annual_df["cpi_mean"],  width=w, label="Avg CPI YoY (%)",
                   color=PALETTE["cpi"],  alpha=0.85, edgecolor="white")
    bars2 = ax.bar(x + w/2, annual_df["repo_mean"], width=w, label="Avg Repo Rate (%)",
                   color=PALETTE["repo"], alpha=0.85, edgecolor="white")

    # Value labels on bars
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{bar.get_height():.1f}", ha="center", va="bottom",
                fontsize=7.5, color=PALETTE["cpi"], fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{bar.get_height():.1f}", ha="center", va="bottom",
                fontsize=7.5, color=PALETTE["repo"], fontweight="bold")

    ax.axhline(4.0, color=PALETTE["neutral"], linestyle="--", linewidth=0.9,
               alpha=0.5, label="RBI Target (4%)")
    ax.axhline(6.0, color=PALETTE["cpi"], linestyle=":", linewidth=0.8, alpha=0.5)

    _style_ax(ax, xlabel="Year", ylabel="% per annum",
              title="Annual Average CPI Inflation vs Repo Rate — India (2014–2025)")
    ax.set_xticks(x)
    ax.set_xticklabels(annual_df["year"].astype(str), rotation=0, fontsize=9)
    ax.set_ylim(0, 11)
    ax.legend(fontsize=9, framealpha=0.85)
    _save(fig, "fig6_annual_bars.png")


# ---------------------------------------------------------------------------
# Figure 7: Monthly CPI heatmap (year × month)
# ---------------------------------------------------------------------------
def fig7_cpi_heatmap(df: pd.DataFrame):
    pivot = df.pivot_table(values="cpi_yoy", index=df["date"].dt.year,
                           columns=df["date"].dt.month)
    pivot.columns = ["Jan","Feb","Mar","Apr","May","Jun",
                     "Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot.index.name = "Year"

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("white")
    sns.heatmap(pivot, ax=ax, cmap="RdYlGn_r", center=4.0, annot=True, fmt=".1f",
                linewidths=0.4, linecolor="#cccccc", cbar_kws={"label": "CPI YoY (%)"},
                annot_kws={"size": 8})
    ax.set_title("Monthly CPI Inflation Heatmap — India (2014–2025)\n"
                 "Red = above 6% | Green = below 4%",
                 fontsize=13, fontweight="bold", color=PALETTE["neutral"], pad=12)
    ax.set_xlabel("Month", fontsize=10)
    ax.set_ylabel("Year", fontsize=10)
    ax.tick_params(labelsize=9)
    _save(fig, "fig7_cpi_heatmap.png")


# ---------------------------------------------------------------------------
# Figure 8: OLS R² across lag models
# ---------------------------------------------------------------------------
def fig8_ols_rsq(results: dict):
    ols = results["ols_results"]
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("white")

    labels = ["Lag 0\n(Contemp.)", "Lag 1m", "Lag 3m", "Lag 6m"]
    bars = ax.bar(labels, ols["r_squared"], color=PALETTE["repo"],
                  alpha=0.85, width=0.45, edgecolor="white")

    for bar, p_val in zip(bars, ols["p_coef_x"]):
        sig = "★★★" if p_val < 0.001 else ("★★" if p_val < 0.01 else ("★" if p_val < 0.05 else ""))
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.003,
                f"R²={bar.get_height():.3f}\n{sig}",
                ha="center", va="bottom", fontsize=9,
                color=PALETTE["neutral"], fontweight="bold")

    _style_ax(ax, xlabel="Lag Model", ylabel="R² (Coefficient of Determination)",
              title="OLS Model Fit: CPI Inflation ~ Repo Rate\nR² by Lag (★ = sig. at 5%, ★★ at 1%, ★★★ at 0.1%)")
    ax.set_ylim(0, max(ols["r_squared"]) * 1.35)
    _save(fig, "fig8_ols_rsquared.png")


# ---------------------------------------------------------------------------
# Master call
# ---------------------------------------------------------------------------
def generate_all_figures(df: pd.DataFrame, annual_df: pd.DataFrame, results: dict):
    print("\n[visualisation] Generating figures...")
    fig1_dual_axis(df)
    fig2_cpi_standalone(df)
    fig3_repo_step(df)
    fig4_scatter_lags(df)
    fig5_crosscorr(results)
    fig6_annual_bars(annual_df)
    fig7_cpi_heatmap(df)
    fig8_ols_rsq(results)
    print(f"[visualisation] All figures saved to: {FIG_DIR}")


if __name__ == "__main__":
    from src.data_processing import run_processing
    from src.analysis import run_analysis
    df, ann = run_processing()
    res = run_analysis(df)
    generate_all_figures(df, ann, res)
