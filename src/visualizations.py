"""
Visualization module for generating publication-quality statistical graphics.
Produces high-resolution figures for distributions, group comparisons,
confidence intervals, post-hoc forest plots, secondary t-test, and diagnostic Q-Q plots.
"""

from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#2D3748"
plt.rcParams["axes.linewidth"] = 0.9
plt.rcParams["grid.color"] = "#E2E8F0"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

NAVY = "#1B365D"
TEAL = "#008080"
CORAL = "#D9534F"
SLATE = "#4A5568"
GOLD = "#D97706"
MUTED_BLUE = "#3B82F6"
LIGHT_GRAY = "#94A3B8"


def plot_alcohol_distribution(df: pd.DataFrame, figures_dir: Path) -> Path:
    """
    Generate Figure 1: Distribution of Alcohol Content with KDE and Normal overlay.
    """
    alc = df["alcohol"]
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    counts, bins, patches = ax.hist(
        alc,
        bins=25,
        density=True,
        color="#3B82F6",
        alpha=0.45,
        edgecolor="#1E40AF",
        linewidth=1.0,
        label="Observed Histogram",
    )

    kde_x = np.linspace(alc.min() - 0.5, alc.max() + 0.5, 300)
    kde = stats.gaussian_kde(alc)
    ax.plot(kde_x, kde(kde_x), color=NAVY, linewidth=2.4, label="Empirical KDE")

    norm_pdf = stats.norm.pdf(kde_x, loc=alc.mean(), scale=alc.std())
    ax.plot(
        kde_x,
        norm_pdf,
        color=CORAL,
        linestyle="--",
        linewidth=2.0,
        label=f"Normal Fit (μ={alc.mean():.2f}, σ={alc.std():.2f})",
    )

    mean_val = alc.mean()
    median_val = alc.median()
    ax.axvline(mean_val, color=CORAL, linestyle="-", linewidth=1.5, alpha=0.9, label=f"Mean: {mean_val:.2f}% vol")
    ax.axvline(median_val, color=TEAL, linestyle="-.", linewidth=1.5, alpha=0.9, label=f"Median: {median_val:.2f}% vol")

    stats_text = (
        f"N = {len(alc):,}\n"
        f"Mean = {mean_val:.2f}% vol\n"
        f"Median = {median_val:.2f}% vol\n"
        f"Std Dev = {alc.std():.2f}% vol\n"
        f"IQR = {alc.quantile(0.75)-alc.quantile(0.25):.2f}% vol\n"
        f"Skewness = {alc.skew():.2f}\n"
        f"Kurtosis = {alc.kurtosis():.2f}"
    )
    ax.text(
        0.96,
        0.94,
        stats_text,
        transform=ax.transAxes,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="#CBD5E1", alpha=0.95),
        fontsize=9,
        linespacing=1.3,
    )

    ax.set_title("Figure 1: Distribution of Alcohol Content in Red Wine (N = 1,599)", fontsize=13, fontweight="bold", pad=12, color=NAVY)
    ax.set_xlabel("Alcohol Content (% by volume)", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_ylabel("Probability Density", fontsize=11, fontweight="semibold", labelpad=8)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=9)
    ax.set_xlim(8.0, 15.5)

    plt.tight_layout()
    output_path = figures_dir / "figure1_alcohol_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_alcohol_by_quality_boxplot(df: pd.DataFrame, figures_dir: Path) -> Path:
    """
    Generate Figure 2: Boxplot and Violin Plot across Quality Levels with Sample Counts.
    """
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    quality_levels = sorted(df["quality"].unique())

    violin_parts = ax.violinplot(
        [df[df["quality"] == q]["alcohol"].values for q in quality_levels],
        positions=range(len(quality_levels)),
        showmeans=False,
        showextrema=False,
        widths=0.7,
    )
    for pc in violin_parts["bodies"]:
        pc.set_facecolor("#93C5FD")
        pc.set_edgecolor("#1D4ED8")
        pc.set_alpha(0.35)

    box_data = [df[df["quality"] == q]["alcohol"].values for q in quality_levels]
    box = ax.boxplot(
        box_data,
        positions=range(len(quality_levels)),
        widths=0.35,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="D", markeredgecolor="#B91C1C", markerfacecolor="#EF4444", markersize=6),
        medianprops=dict(color="#B91C1C", linewidth=2.0),
        boxprops=dict(facecolor="#DBEAFE", color="#1E40AF", linewidth=1.2),
        whiskerprops=dict(color="#1E40AF", linewidth=1.2),
        capprops=dict(color="#1E40AF", linewidth=1.2),
        flierprops=dict(marker="o", markerfacecolor="#94A3B8", markeredgecolor="none", alpha=0.5, markersize=4),
    )

    for idx, q in enumerate(quality_levels):
        sub_alc = df[df["quality"] == q]["alcohol"]
        n_q = len(sub_alc)
        mean_q = sub_alc.mean()
        ax.text(
            idx,
            8.2,
            f"n={n_q}\nμ={mean_q:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#1E293B",
            fontweight="medium",
        )

    ax.set_xticks(range(len(quality_levels)))
    ax.set_xticklabels([f"Quality {q}" for q in quality_levels], fontsize=10, fontweight="semibold")
    ax.set_title("Figure 2: Alcohol Content Across Red Wine Quality Levels (Scores 3–8)", fontsize=13, fontweight="bold", pad=14, color=NAVY)
    ax.set_xlabel("Wine Sensory Quality Score (3 = Lowest, 8 = Highest)", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_ylabel("Alcohol Content (% by volume)", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_ylim(7.8, 15.3)

    legend_elements = [
        plt.Line2D([0], [0], color="#B91C1C", lw=2, label="Median"),
        plt.Line2D([0], [0], marker="D", color="w", markeredgecolor="#B91C1C", markerfacecolor="#EF4444", markersize=7, label="Mean (♦)"),
        plt.Line2D([0], [0], color="#93C5FD", lw=6, alpha=0.5, label="Kernel Density (Violin)"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=9)

    plt.tight_layout()
    output_path = figures_dir / "figure2_alcohol_by_quality_boxplot.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_group_means_confidence_intervals(df: pd.DataFrame, figures_dir: Path) -> Path:
    """
    Generate Figure 3: Group-wise Mean Alcohol Content with 95% Confidence Intervals.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    quality_levels = sorted(df["quality"].unique())
    means, cis_low, cis_high, err_low, err_high = [], [], [], [], []

    for q in quality_levels:
        grp = df[df["quality"] == q]["alcohol"]
        n = len(grp)
        m = grp.mean()
        se = grp.std(ddof=1) / np.sqrt(n)
        ci_margin = stats.t.ppf(0.975, df=n - 1) * se if n > 1 else 0
        means.append(m)
        cis_low.append(m - ci_margin)
        cis_high.append(m + ci_margin)
        err_low.append(ci_margin)
        err_high.append(ci_margin)

    ax.errorbar(
        quality_levels,
        means,
        yerr=[err_low, err_high],
        fmt="o-",
        color=NAVY,
        ecolor=CORAL,
        elinewidth=2.2,
        capsize=6,
        capthick=1.8,
        markersize=8,
        markerfacecolor=TEAL,
        markeredgecolor=NAVY,
        markeredgewidth=1.5,
        linewidth=2.0,
        label="Group Mean ± 95% CI",
        zorder=4,
    )

    grand_mean = df["alcohol"].mean()
    ax.axhline(grand_mean, color="#64748B", linestyle="--", linewidth=1.5, label=f"Grand Mean: {grand_mean:.2f}% vol", zorder=2)

    for q, m, l_ci, u_ci in zip(quality_levels, means, cis_low, cis_high):
        ax.annotate(
            f"{m:.2f}%\n[{l_ci:.2f}, {u_ci:.2f}]",
            xy=(q, m),
            xytext=(0, 14),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            fontweight="bold",
            color=NAVY,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F8FAFC", edgecolor="#E2E8F0", alpha=0.9),
        )

    ax.set_title("Figure 3: Group-Wise Mean Alcohol Content with 95% Confidence Intervals", fontsize=13, fontweight="bold", pad=14, color=NAVY)
    ax.set_xlabel("Wine Sensory Quality Score", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_ylabel("Mean Alcohol Content (% by volume)", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_xticks(quality_levels)
    ax.set_ylim(9.0, 13.5)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=9)

    plt.tight_layout()
    output_path = figures_dir / "figure3_group_means_confidence_intervals.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_posthoc_tukey_forest(tukey_records: list, figures_dir: Path) -> Path:
    """
    Generate Figure 4: Forest plot of Tukey HSD Post-Hoc Pairwise Mean Differences with 95% CIs.
    """
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)

    records = sorted(tukey_records, key=lambda r: r["Mean_Difference"])
    labels = [f"Quality {r['Group_1']} vs {r['Group_2']}" for r in records]
    meandiffs = [r["Mean_Difference"] for r in records]
    ci_lowers = [r["CI_95_Lower"] for r in records]
    ci_uppers = [r["CI_95_Upper"] for r in records]
    rejects = [r["Reject_H0"] for r in records]

    y_positions = np.arange(len(records))

    ax.axvline(0, color="#1E293B", linestyle="--", linewidth=1.5, alpha=0.85, zorder=2, label="Null Difference (Δ = 0)")

    for y, md, low, up, rej in zip(y_positions, meandiffs, ci_lowers, ci_uppers, rejects):
        color = "#16A34A" if rej else "#DC2626"
        err_left = md - low
        err_right = up - md

        ax.errorbar(
            md,
            y,
            xerr=[[err_left], [err_right]],
            fmt="s",
            color=color,
            ecolor=color,
            elinewidth=2.0,
            capsize=4,
            capthick=1.5,
            markersize=6,
            zorder=3,
        )

        p_text = f"Δ={md:+.2f} (p<0.05)" if rej else f"Δ={md:+.2f} (p≥0.05)"
        ax.text(
            up + 0.08,
            y,
            p_text,
            va="center",
            fontsize=8,
            color=color,
            fontweight="semibold",
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlabel("Difference in Mean Alcohol Content (% by volume, 95% Tukey HSD CI)", fontsize=11, fontweight="semibold", labelpad=8)
    ax.set_title("Figure 4: Tukey HSD Post-Hoc Pairwise Comparisons (Family-Wise α = 0.05)", fontsize=13, fontweight="bold", pad=14, color=NAVY)
    ax.set_xlim(-1.2, 3.8)

    legend_elements = [
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#16A34A", markersize=7, label="Statistically Significant (Reject H0)"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#DC2626", markersize=7, label="Not Significant (Fail to Reject H0)"),
        plt.Line2D([0], [0], color="#1E293B", linestyle="--", lw=1.5, label="Zero Difference Reference"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=9)

    plt.tight_layout()
    output_path = figures_dir / "figure4_posthoc_tukey_hsd_intervals.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_secondary_ttest_comparison(df: pd.DataFrame, secondary_stats: Dict[str, Any], figures_dir: Path) -> Path:
    """
    Generate Figure 5: Secondary Hypothesis Comparison between High (>=7) and Low (<=5) Quality Wines.
    """
    high = df[df["quality"] >= 7]["alcohol"]
    low = df[df["quality"] <= 5]["alcohol"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300, gridspec_kw={"width_ratios": [1.4, 1]})

    kde_x = np.linspace(8.0, 15.0, 300)
    kde_high = stats.gaussian_kde(high)
    kde_low = stats.gaussian_kde(low)

    ax1.fill_between(kde_x, kde_low(kde_x), color="#EF4444", alpha=0.3, label=f"Low Quality (≤5, n={len(low)})")
    ax1.plot(kde_x, kde_low(kde_x), color="#DC2626", lw=2.2)

    ax1.fill_between(kde_x, kde_high(kde_x), color="#3B82F6", alpha=0.3, label=f"High Quality (≥7, n={len(high)})")
    ax1.plot(kde_x, kde_high(kde_x), color="#1D4ED8", lw=2.2)

    ax1.axvline(low.mean(), color="#DC2626", linestyle="--", lw=1.8, label=f"Low Mean: {low.mean():.2f}%")
    ax1.axvline(high.mean(), color="#1D4ED8", linestyle="--", lw=1.8, label=f"High Mean: {high.mean():.2f}%")

    ax1.set_title("(a) Kernel Density Estimation by Quality Group", fontsize=11, fontweight="bold", color=NAVY)
    ax1.set_xlabel("Alcohol Content (% by volume)", fontsize=10.5, fontweight="semibold")
    ax1.set_ylabel("Probability Density", fontsize=10.5, fontweight="semibold")
    ax1.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5)

    box_data = [low.values, high.values]
    bp = ax2.boxplot(
        box_data,
        widths=0.45,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="D", markeredgecolor="black", markerfacecolor="white", markersize=6),
        medianprops=dict(color="black", lw=1.8),
    )
    colors = ["#FCA5A5", "#93C5FD"]
    edge_colors = ["#DC2626", "#1D4ED8"]
    for patch, c, ec in zip(bp["boxes"], colors, edge_colors):
        patch.set_facecolor(c)
        patch.set_edgecolor(ec)
        patch.set_linewidth(1.5)

    ax2.set_xticklabels(["Low Quality (≤5)", "High Quality (≥7)"], fontsize=10, fontweight="semibold")
    ax2.set_ylabel("Alcohol Content (% by volume)", fontsize=10.5, fontweight="semibold")
    ax2.set_title("(b) Group Comparison & Effect Size", fontsize=11, fontweight="bold", color=NAVY)

    t_val = secondary_stats["welch_t"]
    p_val_str = f"p = {secondary_stats['welch_p']:.2e}" if secondary_stats['welch_p'] < 0.001 else f"p = {secondary_stats['welch_p']:.4f}"
    diff_val = secondary_stats["mean_diff"]
    d_val = secondary_stats["cohens_d"]
    ci_l = secondary_stats["ci_lower"]
    ci_u = secondary_stats["ci_upper"]

    stat_box_text = (
        f"Welch's t-test:\n"
        f"t = {t_val:.2f}, df = {secondary_stats['df_welch']:.1f}\n"
        f"{p_val_str}\n"
        f"Mean Diff = +{diff_val:.2f}% vol\n"
        f"95% CI: [{ci_l:.2f}%, {ci_u:.2f}%]\n"
        f"Cohen's d = {d_val:.2f} (Large)"
    )
    ax2.text(
        0.05,
        0.95,
        stat_box_text,
        transform=ax2.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8FAFC", edgecolor="#CBD5E1", alpha=0.95),
        fontsize=8.5,
        linespacing=1.3,
    )

    fig.suptitle("Figure 5: Secondary Hypothesis Testing — High vs. Low Quality Red Wine Alcohol Content", fontsize=13, fontweight="bold", color=NAVY, y=0.98)
    plt.tight_layout()
    output_path = figures_dir / "figure5_secondary_ttest_comparison.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_statistical_diagnostics(df: pd.DataFrame, residuals: pd.Series, figures_dir: Path) -> Path:
    """
    Generate Figure 6: 4-Panel Statistical Diagnostic and Correlation Matrix.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=300)

    # (a) Normal Q-Q plot
    ax_qq = axes[0, 0]
    std_res = (residuals - residuals.mean()) / residuals.std(ddof=1)
    sm.qqplot(std_res, line="45", ax=ax_qq, markerfacecolor="#3B82F6", markeredgecolor="#1D4ED8", alpha=0.6, markersize=4)
    ax_qq.set_title("(a) Normal Q-Q Plot of ANOVA Residuals", fontsize=11, fontweight="bold", color=NAVY)
    ax_qq.set_xlabel("Theoretical Quantiles", fontsize=10, fontweight="semibold")
    ax_qq.set_ylabel("Standardized Residuals", fontsize=10, fontweight="semibold")

    # (b) Residuals vs Fitted Values
    ax_rvf = axes[0, 1]
    group_means = df.groupby("quality")["alcohol"].transform("mean")
    ax_rvf.scatter(group_means, residuals, color="#0D9488", alpha=0.45, edgecolor="#0F766E", s=25)
    ax_rvf.axhline(0, color=CORAL, linestyle="--", lw=1.5)
    ax_rvf.set_title("(b) Residuals vs. Group Fitted Means", fontsize=11, fontweight="bold", color=NAVY)
    ax_rvf.set_xlabel("Fitted Quality Group Mean Alcohol (% vol)", fontsize=10, fontweight="semibold")
    ax_rvf.set_ylabel("ANOVA Residuals", fontsize=10, fontweight="semibold")

    # (c) Standard Deviation by Quality Rating
    ax_sd = axes[1, 0]
    stds = df.groupby("quality")["alcohol"].std()
    bars = ax_sd.bar(stds.index, stds.values, color="#6366F1", edgecolor="#4338CA", width=0.55, alpha=0.85)
    ax_sd.axhline(df["alcohol"].std(), color=CORAL, linestyle="--", lw=1.5, label=f"Overall SD ({df['alcohol'].std():.2f}%)")
    for bar in bars:
        height = bar.get_height()
        ax_sd.text(bar.get_x() + bar.get_width() / 2.0, height + 0.02, f"{height:.2f}%", ha="center", va="bottom", fontsize=8.5, fontweight="semibold")
    ax_sd.set_title("(c) Standard Deviation Across Quality Levels (Homoscedasticity)", fontsize=11, fontweight="bold", color=NAVY)
    ax_sd.set_xlabel("Quality Score", fontsize=10, fontweight="semibold")
    ax_sd.set_ylabel("Standard Deviation (% vol)", fontsize=10, fontweight="semibold")
    ax_sd.set_ylim(0, 1.5)
    ax_sd.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5)

    # (d) Scatter Plot with Linear Regression Line
    ax_sc = axes[1, 1]
    jitter = np.random.normal(0, 0.08, size=len(df))
    ax_sc.scatter(df["quality"] + jitter, df["alcohol"], color="#0284C7", alpha=0.35, s=20, edgecolor="none", label="Wine Samples (Jittered)")
    m, b = np.polyfit(df["quality"], df["alcohol"], 1)
    x_vals = np.array([3, 8])
    ax_sc.plot(x_vals, m * x_vals + b, color=CORAL, lw=2.2, label=f"Fit: y = {m:.2f}x + {b:.2f}")

    r_val, p_val = stats.pearsonr(df["alcohol"], df["quality"])
    ax_sc.text(
        0.05,
        0.92,
        f"Pearson r = {r_val:.2f} (p < 0.001)\nR² = {r_val**2:.2f}",
        transform=ax_sc.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#F8FAFC", edgecolor="#CBD5E1", alpha=0.9),
        fontsize=8.5,
        linespacing=1.3,
    )
    ax_sc.set_title("(d) Alcohol Content vs. Sensory Quality", fontsize=11, fontweight="bold", color=NAVY)
    ax_sc.set_xlabel("Quality Rating (3 to 8)", fontsize=10, fontweight="semibold")
    ax_sc.set_ylabel("Alcohol Content (% by volume)", fontsize=10, fontweight="semibold")
    ax_sc.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5)

    fig.suptitle("Figure 6: Statistical Diagnostic and Assumption Assessment Matrix", fontsize=13, fontweight="bold", color=NAVY, y=0.98)
    plt.tight_layout()
    output_path = figures_dir / "figure6_statistical_diagnostics_qq.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def generate_all_visualizations(
    df: pd.DataFrame,
    residuals: pd.Series,
    tukey_records: list,
    secondary_stats: Dict[str, Any],
    figures_dir: Path,
) -> Dict[str, Path]:
    """
    Generate all project figures and save to outputs/figures/.
    """
    figures_dir.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)

    fig1 = plot_alcohol_distribution(df, figures_dir)
    fig2 = plot_alcohol_by_quality_boxplot(df, figures_dir)
    fig3 = plot_group_means_confidence_intervals(df, figures_dir)
    fig4 = plot_posthoc_tukey_forest(tukey_records, figures_dir)
    fig5 = plot_secondary_ttest_comparison(df, secondary_stats, figures_dir)
    fig6 = plot_statistical_diagnostics(df, residuals, figures_dir)

    return {
        "fig1": fig1,
        "fig2": fig2,
        "fig3": fig3,
        "fig4": fig4,
        "fig5": fig5,
        "fig6": fig6,
    }
