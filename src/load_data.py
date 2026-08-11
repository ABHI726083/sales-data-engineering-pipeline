import sys
import pandas as pd


# ==========================================
# REQUIRED COLUMNS
# ==========================================

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product",
    "category",
    "quantity",
    "price",
    "city"
]


# ==========================================
# CHECK INPUT FILE
# ==========================================

if len(sys.argv) < 2:

    print("ERROR: Please provide a CSV file path.")
    print("Example:")
    print("python run_pipeline.py data/sales.csv")

    sys.exit(1)


# ==========================================
# GET FILE PATH
# ==========================================

file_path = sys.argv[1]

print("Input file:", file_path)


# ==========================================
# LOAD CSV
# ==========================================

try:

    df = pd.read_csv(file_path)

except FileNotFoundError:

    print("\n❌ ERROR: CSV file not found!")
    print("File:", file_path)

    sys.exit(1)

except pd.errors.EmptyDataError:

    print("\n❌ ERROR: CSV file is empty!")
    print("File:", file_path)

    sys.exit(1)

except pd.errors.ParserError:

    print("\n❌ ERROR: CSV file could not be read!")
    print("The file may be malformed.")

    sys.exit(1)


# ==========================================
# CHECK REQUIRED COLUMNS
# ==========================================

print("\nChecking required columns...")


missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]


# ==========================================
# STOP IF COLUMNS ARE MISSING
# ==========================================

if missing_columns:

    print("\n❌ DATA SCHEMA ERROR")

    print("Missing columns:")

    for column in missing_columns:
        print("-", column)

    print("\nRequired columns:")

    for column in REQUIRED_COLUMNS:
        print("-", column)

    print("\nActual columns found:")

    for column in df.columns:
        print("-", column)

    sys.exit(1)


print("Required columns: OK")


# ==========================================
# CHECK FOR COMPLETELY EMPTY DATASET
# ==========================================

if df.empty:

    print("\n❌ DATA ERROR")
    print("CSV contains no data rows.")

    sys.exit(1)


# ==========================================
# SHOW DATA
# ==========================================

print("\nData loaded successfully!")

print(df)

print("\nRows:", len(df))

print("Columns:", list(df.columns))