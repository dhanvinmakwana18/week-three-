# Main execution script for Week 3 Statistical Analysis and Hypothesis Testing.
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

import data_loader
import data_cleaning
import statistical_analysis
import visualizations
import report_generator


def run_pipeline() -> None:
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    outputs_dir = project_root / "outputs"
    tables_dir = outputs_dir / "tables"
    figures_dir = outputs_dir / "figures"
    report_dir = project_root / "report"
    report_path = report_dir / "Week_3_Statistical_Analysis_Hypothesis_Testing.docx"

    for d in [data_dir / "raw", data_dir / "processed", tables_dir, figures_dir, report_dir]:
        d.mkdir(parents=True, exist_ok=True)

    print("[1/5] Ingesting UCI Wine Quality dataset...")
    raw_df = data_loader.load_raw_data(data_dir)
    print(f"      Loaded raw dataset: {len(raw_df):,} rows, {raw_df.shape[1]} columns.")

    print("[2/5] Cleaning and preparing data...")
    clean_df, clean_summary = data_cleaning.clean_and_prepare_data(raw_df, data_dir)
    print(f"      Cleaned dataset saved: {len(clean_df):,} observations, 0 missing values.")

    print("[3/5] Performing statistical analysis and hypothesis testing...")
    desc_stats = statistical_analysis.compute_descriptive_statistics(clean_df, tables_dir)
    assumption_stats = statistical_analysis.evaluate_statistical_assumptions(clean_df, tables_dir)
    primary_stats = statistical_analysis.perform_primary_hypothesis_test(clean_df, tables_dir)
    tukey_stats = statistical_analysis.perform_posthoc_tukey_hsd(clean_df, tables_dir)
    secondary_stats = statistical_analysis.perform_secondary_hypothesis_test(clean_df, tables_dir)

    print(f"      One-Way ANOVA: F({primary_stats['df_between']}, {primary_stats['df_within']}) = {primary_stats['f_stat']:.2f}, p = {primary_stats['p_value']:.2e}, eta2 = {primary_stats['eta_squared']:.4f}")
    print(f"      Welch t-test: t({secondary_stats['df_welch']:.1f}) = {secondary_stats['welch_t']:.2f}, p = {secondary_stats['welch_p']:.2e}, Cohen d = {secondary_stats['cohens_d']:.2f}")

    print("[4/5] Generating publication-quality visualizations...")
    figures_dict = visualizations.generate_all_visualizations(
        clean_df,
        assumption_stats["residuals"],
        tukey_stats["tukey_records"],
        secondary_stats,
        figures_dir,
    )
    print(f"      Generated {len(figures_dict)} high-resolution figures in {figures_dir}.")

    print("[5/5] Compiling academic DOCX report...")
    summary_data = {
        "clean_summary": clean_summary,
        "desc_stats": desc_stats,
        "assumption_stats": assumption_stats,
        "primary_stats": primary_stats,
        "tukey_stats": tukey_stats,
        "secondary_stats": secondary_stats,
    }
    final_report = report_generator.build_docx_report(report_path, summary_data, figures_dict)
    print(f"      Report compiled successfully: {final_report}")
    print("Execution complete. All artifacts generated successfully.")


if __name__ == "__main__":
    run_pipeline()
