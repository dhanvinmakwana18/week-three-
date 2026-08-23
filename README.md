# Week 3 ? Statistical Analysis & Hypothesis Testing

An end-to-end, reproducible inferential data science project investigating the physicochemical determinants of sensory wine quality via One-Way Analysis of Variance (ANOVA), Tukey HSD post-hoc multiple comparisons, and Welch's independent samples t-tests in Python.

---

## Research Question

**Does mean alcohol content differ across red wine quality ratings?**

- **Null Hypothesis ($H_0$):** Population mean alcohol content is identical across all quality levels (scores 3 through 8):
  $$\mu_3 = \mu_4 = \mu_5 = \mu_6 = \mu_7 = \mu_8$$
- **Alternative Hypothesis ($H_1$):** At least one quality level possesses a different population mean alcohol content:
  $$\exists i, j \in \{3, 4, 5, 6, 7, 8\} \quad \text{such that} \quad \mu_i \neq \mu_j$$
- **Significance Level:** $\alpha = 0.05$

---

## Secondary Research Question

**Do high-quality wines ($\text{quality} \ge 7$) have significantly higher mean alcohol content than low-to-moderate quality wines ($\text{quality} \le 5$)?**

- **Null Hypothesis ($H_{0,\text{sec}}$):** $\mu_{\text{high}} = \mu_{\text{low}}$
- **Alternative Hypothesis ($H_{1,\text{sec}}$):** $\mu_{\text{high}} \neq \mu_{\text{low}}$
- **Significance Level:** $\alpha = 0.05$

---

## Dataset

- **Dataset:** UCI Wine Quality ? Red Wine dataset
- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- **Reference:** Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). *Modeling wine preferences by data mining from physicochemical properties*. Decision Support Systems, 47(4), 547-553.
- **Sample Size:** $N = 1,599$ observations ($100\%$ complete, $0$ missing values).
- **Attributes:** 11 continuous physicochemical features + 1 discrete sensory quality rating (scale 0?10).

---

## Statistical Methods

The analytical pipeline implements:

- **Descriptive statistics:** Group-wise and overall sample size ($n$), mean ($\bar{x}$), standard deviation ($s$), variance ($s^2$), median, interquartile range (IQR), skewness, and kurtosis.
- **95% confidence intervals:** Student's $t$ confidence intervals for group means and differences.
- **Assumption diagnostics:**
  - Normality of residuals evaluated via Shapiro-Wilk ($W = 0.9670, p < 0.001$) and Kolmogorov-Smirnov tests alongside Normal Q-Q diagnostics.
  - Homogeneity of variance evaluated via median-centered Levene's test ($W = 24.23, p < 0.001$) and Bartlett's test ($T = 85.74, p < 0.001$).
  - Observational independence verified by production design and randomized sensory protocols.
- **One-Way ANOVA:** Parametric omnibus $F$-test across 6 quality levels ($F = 115.85, p < 0.001$).
- **Eta-squared ($\eta^2$):** Proportion of sample variance explained ($\eta^2 = 0.2667$).
- **Omega-squared ($\omega^2$):** Population-level effect size adjusted for sample bias ($\omega^2 = 0.2642$, very large effect).
- **Kruskal-Wallis test:** Non-parametric rank-based omnibus test ($H(5) = 412.38, p < 0.001$).
- **Tukey HSD:** Multiple pairwise comparisons controlling the Family-Wise Error Rate ($\text{FWER} \le 0.05$) across all 15 group contrasts.
- **Welch's independent t-test:** Two-sample test with Welch-Satterthwaite adjusted degrees of freedom for heterogeneous variances ($t(292.4) = 21.73, p < 0.001$).
- **Cohen's d:** Standardized effect size ($d = 1.95$).
- **Hedges' g:** Small-sample corrected standardized effect size ($g = 1.94$).
- **Mann-Whitney U test:** Non-parametric two-sample rank test ($U = 145,136.0, p < 0.001$).
- **Pearson correlation:** Bivariate linear association ($r = 0.4762, p < 0.001, R^2 = 0.2268$).
- **Spearman correlation:** Bivariate monotonic rank correlation ($\rho = 0.4785, p < 0.001$).
- **Diagnostic visualization:** 6 publication-ready figures ($300$ DPI) covering histograms, violin plots, confidence intervals, Tukey HSD forest plots, KDE contrasts, and a 4-panel diagnostic matrix.

---

## Key Results

### One-Way ANOVA
- **F-statistic:** $F(5, 1593) = 115.85$
- **p-value:** $p = 1.21 \times 10^{-104} < 0.001$
- **Eta-squared ($\eta^2$):** $0.2667$ ($26.67\%$ of total variance explained)
- **Omega-squared ($\omega^2$):** $0.2642$ ($26.42\%$ of population variance explained)
- **Decision:** **Reject $H_0$** (Overwhelming evidence of alcohol differences across quality levels)

### Welch's t-Test (High Quality $\ge 7$ vs. Low Quality $\le 5$)
- **t-statistic:** $t(292.4) = 21.73$
- **p-value:** $p = 5.44 \times 10^{-63} < 0.001$
- **Mean difference:** $+1.59\%$ vol ($\text{High Mean} = 11.52\% \text{ vs. Low Mean} = 9.93\%$)
- **95% Confidence Interval:** $[1.45\%, 1.74\%]$
- **Cohen's d:** $1.95$ (Substantial practical effect)
- **Decision:** **Reject $H_{0,\text{sec}}$** (High-quality wines possess significantly higher ethanol content)

---

## Project Structure

```text
week3-statistical-analysis-hypothesis-testing/
??? data/
?   ??? raw/
?   ?   ??? winequality-red.csv                          # Cached raw UCI dataset
?   ??? processed/
?       ??? winequality_cleaned.csv                      # Cleaned dataset with analytical tiers
??? outputs/
?   ??? figures/
?   ?   ??? figure1_alcohol_distribution.png             # Overall alcohol density and normal fit
?   ?   ??? figure2_alcohol_by_quality_boxplot.png       # Violin density and quartile boxplots
?   ?   ??? figure3_group_means_confidence_intervals.png # Group means with 95% CIs
?   ?   ??? figure4_posthoc_tukey_hsd_intervals.png      # Tukey HSD pairwise forest plot
?   ?   ??? figure5_secondary_ttest_comparison.png       # Welch t-test KDE & boxplot comparison
?   ?   ??? figure6_statistical_diagnostics_qq.png       # 4-panel Q-Q and homoscedasticity diagnostic
?   ??? tables/
?       ??? table1_descriptive_statistics_by_quality.csv # Group-wise descriptive statistics
?       ??? table2_overall_descriptive_statistics.csv    # Total sample descriptive statistics
?       ??? table3_assumption_checks.csv                 # Normality and homoscedasticity results
?       ??? table4_anova_results.csv                     # ANOVA table and effect sizes
?       ??? table5_posthoc_tukey_hsd.csv                 # All 15 Tukey pairwise comparisons
?       ??? table6_secondary_test_results.csv            # Welch t-test and Mann-Whitney results
?       ??? table7_correlation_analysis.csv              # Pearson and Spearman correlations
??? report/
?   ??? Week_3_Statistical_Analysis_Hypothesis_Testing.docx # Comprehensive 22-section DOCX report
??? src/
?   ??? data_loader.py                                   # Programmatic ingestion and caching
?   ??? data_cleaning.py                                 # Auditing, IQR checks, and tier labeling
?   ??? statistical_analysis.py                          # Complete parametric & non-parametric tests
?   ??? visualizations.py                                # 300 DPI publication-grade plotting
?   ??? report_generator.py                              # DOCX compilation with styled tables & figures
?   ??? main.py                                          # Master pipeline orchestrator
??? .gitignore                                           # Git exclusion rules
??? README.md                                            # Technical documentation
??? requirements.txt                                     # Pinned dependency specifications
```

---

## Reproducibility

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Standard internet connection for initial dataset download

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Execute Analysis Pipeline
```bash
python src/main.py
```

The script will automatically:
1. Ingest and validate the UCI Red Wine Quality dataset
2. Clean data and compute IQR fences
3. Run all descriptive, diagnostic, ANOVA, Tukey HSD, and Welch $t$-tests, saving CSV tables to `outputs/tables/`
4. Generate 6 high-resolution figures in `outputs/figures/`
5. Compile the comprehensive academic DOCX report in `report/`

---

## Report

The final comprehensive, 22-section technical statistical report is located at:

```text
report/Week_3_Statistical_Analysis_Hypothesis_Testing.docx
```

---

## References

1. Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems*, 47(4), 547-553.
2. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
3. Tukey, J. W. (1949). Comparing individual means in the analysis of variance. *Biometrics*, 5(2), 99-114.
4. Welch, B. L. (1947). The generalization of 'Student's' problem when several different population variances are involved. *Biometrika*, 34(1/2), 28-35.
5. Virtanen, P., et al. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. *Nature Methods*, 17(3), 261-272.
