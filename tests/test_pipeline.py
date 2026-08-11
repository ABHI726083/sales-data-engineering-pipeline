import subprocess
import sys
from pathlib import Path


# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ==========================================
# TEST COMPLETE PIPELINE
# ==========================================

def test_complete_pipeline():

    input_file = PROJECT_ROOT / "data" / "sales.csv"

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "run_pipeline.py"),
            str(input_file)
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    # ==========================================
    # PIPELINE MUST COMPLETE SUCCESSFULLY
    # ==========================================

    assert result.returncode == 0, (
        f"Pipeline failed.\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )

    # ==========================================
    # CHECK PIPELINE OUTPUT
    # ==========================================

    assert "PIPELINE STARTED" in result.stdout

    assert "STEP 1: LOAD RAW DATA" in result.stdout

    assert "STEP 2: CLEAN DATA" in result.stdout

    assert "STEP 3: VALIDATE DATA" in result.stdout

    assert "STEP 4: LOAD INTO POSTGRESQL" in result.stdout

    assert "STEP 5: RUN ANALYTICS" in result.stdout

    assert "STEP 6: GENERATE REPORTS" in result.stdout

    assert "PIPELINE COMPLETED SUCCESSFULLY!" in result.stdout


# ==========================================
# TEST CLEANED OUTPUT
# ==========================================

def test_cleaned_file_created():

    cleaned_file = (
        PROJECT_ROOT
        / "output"
        / "cleaned_sales.csv"
    )

    assert cleaned_file.exists()

    assert cleaned_file.stat().st_size > 0


# ==========================================
# TEST REPORT DIRECTORY
# ==========================================

def test_reports_created():

    reports_directory = (
        PROJECT_ROOT
        / "output"
        / "reports"
    )

    assert reports_directory.exists()

    assert reports_directory.is_dir()


# ==========================================
# TEST REQUIRED REPORTS
# ==========================================

def test_required_reports_exist():

    reports_directory = (
        PROJECT_ROOT
        / "output"
        / "reports"
    )

    required_reports = [
        "pipeline_summary.csv",
        "sales_by_city.csv",
        "sales_by_category.csv",
        "sales_by_product.csv",
        "quantity_by_product.csv"
    ]

    for report in required_reports:

        report_file = reports_directory / report

        assert report_file.exists(), (
            f"Missing report: {report}"
        )

        assert report_file.stat().st_size > 0