import os
import subprocess
import sys
from pathlib import Path


# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VALIDATE_SCRIPT = (
    PROJECT_ROOT /
    "src" /
    "validate_data.py"
)


# ==========================================
# RUN VALIDATION SCRIPT
# ==========================================

def run_validator(csv_file):

    environment = os.environ.copy()

    # Allow project imports if needed
    environment["PYTHONPATH"] = str(PROJECT_ROOT)

    # Force UTF-8 output for Windows
    environment["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATE_SCRIPT),
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
# CREATE VALID CSV
# ==========================================

def create_valid_csv(path):

    path.write_text(
        """order_id,order_date,product,category,quantity,price,city,total_sales
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi,100000
2002,2026-02-02,Mouse,Electronics,5,800,Noida,4000
""",
        encoding="utf-8"
    )


# ==========================================
# TEST 1: VALID DATA
# ==========================================

def test_valid_data(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    create_valid_csv(input_file)

    result = run_validator(input_file)

    assert result.returncode == 0, (
        f"\nSTDOUT:\n{result.stdout}"
        f"\nSTDERR:\n{result.stderr}"
    )

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "DATA VALIDATION PASSED" in combined_output


# ==========================================
# TEST 2: DUPLICATE ORDER ID
# ==========================================

def test_duplicate_order_id(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city,total_sales
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi,100000
2001,2026-02-02,Mouse,Electronics,5,800,Noida,4000
""",
        encoding="utf-8"
    )

    result = run_validator(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "Duplicate order IDs detected" in combined_output


# ==========================================
# TEST 3: INVALID QUANTITY
# ==========================================

def test_invalid_quantity(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city,total_sales
2001,2026-02-01,Laptop,Electronics,-2,50000,Delhi,-100000
""",
        encoding="utf-8"
    )

    result = run_validator(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "Quantity must be a positive integer" in combined_output


# ==========================================
# TEST 4: INVALID PRICE
# ==========================================

def test_invalid_price(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city,total_sales
2001,2026-02-01,Laptop,Electronics,2,-50000,Delhi,-100000
""",
        encoding="utf-8"
    )

    result = run_validator(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "Price must be a non-negative number" in combined_output


# ==========================================
# TEST 5: INVALID TOTAL SALES
# ==========================================

def test_invalid_total_sales(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city,total_sales
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi,50000
""",
        encoding="utf-8"
    )

    result = run_validator(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert (
        "total_sales does not match quantity"
        in combined_output
    )


# ==========================================
# TEST 6: INVALID DATE
# ==========================================

def test_invalid_date(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city,total_sales
2001,INVALID_DATE,Laptop,Electronics,2,50000,Delhi,100000
""",
        encoding="utf-8"
    )

    result = run_validator(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "Invalid order dates detected" in combined_output


# ==========================================
# TEST 7: MISSING COLUMN
# ==========================================

def test_missing_column(tmp_path):

    input_file = tmp_path / "cleaned_sales.csv"

    input_file.write_text(
        """order_id,order_date,product,category,quantity,price,city
2001,2026-02-01,Laptop,Electronics,2,50000,Delhi
""",
        encoding="utf-8"
    )

    result = run_validator(input_file)

    assert result.returncode != 0

    combined_output = (
        result.stdout +
        result.stderr
    )

    assert "DATA SCHEMA ERROR" in combined_output