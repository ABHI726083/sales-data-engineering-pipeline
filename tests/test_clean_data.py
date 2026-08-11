import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLEAN_SCRIPT = PROJECT_ROOT / "src" / "clean_data.py"

OUTPUT_FILE = (
    PROJECT_ROOT /
    "output" /
    "cleaned_sales.csv"
)


# ==========================================
# RUN CLEANING SCRIPT
# ==========================================

def run_cleaner(csv_file):

    environment = os.environ.copy()

    # Allow clean_data.py to find config.settings
    environment["PYTHONPATH"] = str(PROJECT_ROOT)

    # Force UTF-8 output
    environment["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [
            sys.executable,
            str(CLEAN_SCRIPT),
            str(csv_file)
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment
    )

    return result


# ==========================================
# TEST 1: VALID CSV
# ==========================================

def test_valid_csv(tmp_path):

    input_file = tmp_path / "sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi
2002,2026-02-02,Mouse,Electronics,5,800,Noida
""",
        encoding="utf-8"
    )

    result = run_cleaner(input_file)

    assert result.returncode == 0, (
        f"\nSTDOUT:\n{result.stdout}"
        f"\nSTDERR:\n{result.stderr}"
    )

    assert OUTPUT_FILE.exists()

    df = pd.read_csv(OUTPUT_FILE)

    assert len(df) == 2

    assert "total_sales" in df.columns

    assert df.loc[0, "total_sales"] == 100000
    assert df.loc[1, "total_sales"] == 4000


# ==========================================
# TEST 2: DUPLICATE ROW REMOVAL
# ==========================================

def test_duplicate_rows_removed(tmp_path):

    input_file = tmp_path / "sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi
2002,2026-02-02,Mouse,Electronics,5,800,Noida
""",
        encoding="utf-8"
    )

    result = run_cleaner(input_file)

    assert result.returncode == 0, (
        f"\nSTDOUT:\n{result.stdout}"
        f"\nSTDERR:\n{result.stderr}"
    )

    df = pd.read_csv(OUTPUT_FILE)

    assert len(df) == 2


# ==========================================
# TEST 3: INVALID VALUES REMOVED
# ==========================================

def test_invalid_values_removed(tmp_path):

    input_file = tmp_path / "sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi
2002,2026-02-02,Mouse,Electronics,-5,800,Noida
2003,2026-02-03,Keyboard,Electronics,3,-100,Delhi
2004,2026-02-04,Monitor,Electronics,0,12000,Delhi
""",
        encoding="utf-8"
    )

    result = run_cleaner(input_file)

    assert result.returncode == 0, (
        f"\nSTDOUT:\n{result.stdout}"
        f"\nSTDERR:\n{result.stderr}"
    )

    df = pd.read_csv(OUTPUT_FILE)

    assert len(df) == 1

    assert df.iloc[0]["order_id"] == 2001


# ==========================================
# TEST 4: MISSING REQUIRED COLUMN
# ==========================================

def test_missing_required_column(tmp_path):

    input_file = tmp_path / "sales.csv"

    input_file.write_text(
        """order_id,order_date,product,quantity,price,city
2001,2026-02-01,Laptop,2,50000,Delhi
""",
        encoding="utf-8"
    )

    result = run_cleaner(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "Missing required columns" in combined_output