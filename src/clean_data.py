import sys
from pathlib import Path

import pandas as pd

from config.settings import CLEANED_DATA_FILE


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
# PRINT ERROR AND EXIT
# ==========================================

def fail(message):
    print(f"\n❌ ERROR: {message}")
    sys.exit(1)


# ==========================================
# GET INPUT FILE
# ==========================================

if len(sys.argv) < 2:

    print("ERROR: Please provide a CSV file path.")
    print("Example:")
    print("python clean_data.py data/sales.csv")

    sys.exit(1)


input_file = Path(sys.argv[1])


# ==========================================
# CHECK INPUT FILE
# ==========================================

print(f"Input file: {input_file}")

if not input_file.is_file():

    fail(
        f"Input CSV file not found: {input_file}"
    )


# ==========================================
# LOAD RAW DATA
# ==========================================

print("\nLoading raw data...")

try:

    df = pd.read_csv(input_file)

except pd.errors.EmptyDataError:

    fail("CSV file is empty.")

except pd.errors.ParserError as error:

    fail(f"CSV file could not be parsed: {error}")

except Exception as error:

    fail(f"Could not read CSV file: {error}")


# ==========================================
# CHECK EMPTY DATAFRAME
# ==========================================

if df.empty:

    fail("CSV file contains no data rows.")


original_rows = len(df)

print("Original rows:", original_rows)


# ==========================================
# CHECK REQUIRED COLUMNS
# ==========================================

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:

    print("\n❌ ERROR: Missing required columns:")

    for column in missing_columns:
        print(f"- {column}")

    sys.exit(1)


# ==========================================
# KEEP ONLY EXPECTED COLUMNS
# ==========================================

df = df[REQUIRED_COLUMNS].copy()


# ==========================================
# REMOVE EMPTY ROWS
# ==========================================

before_empty_removal = len(df)

df = df.dropna(
    how="all"
).copy()

empty_rows_removed = (
    before_empty_removal - len(df)
)

print(
    "Empty rows removed:",
    empty_rows_removed
)


# ==========================================
# REMOVE EXACT DUPLICATE ROWS
# ==========================================

before_duplicate_removal = len(df)

df = df.drop_duplicates(
    keep="first"
).copy()

duplicate_rows_removed = (
    before_duplicate_removal - len(df)
)

print(
    "Duplicate rows removed:",
    duplicate_rows_removed
)


# ==========================================
# CLEAN TEXT COLUMNS
# ==========================================

text_columns = [
    "product",
    "category",
    "city"
]

for column in text_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# ==========================================
# CONVERT ORDER ID
# ==========================================

df["order_id"] = pd.to_numeric(
    df["order_id"],
    errors="coerce"
)


# ==========================================
# CONVERT QUANTITY
# ==========================================

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)


# ==========================================
# CONVERT PRICE
# ==========================================

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)


# ==========================================
# CONVERT DATE
# ==========================================

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)


# ==========================================
# REMOVE INVALID REQUIRED VALUES
# ==========================================

before_invalid_removal = len(df)

df = df.dropna(
    subset=[
        "order_id",
        "order_date",
        "product",
        "category",
        "quantity",
        "price",
        "city"
    ]
).copy()

invalid_rows_removed = (
    before_invalid_removal - len(df)
)

if invalid_rows_removed > 0:

    print(
        "Invalid rows removed:",
        invalid_rows_removed
    )


# ==========================================
# VALIDATE POSITIVE VALUES
# ==========================================

invalid_quantity = (
    df["quantity"] <= 0
)

invalid_price = (
    df["price"] < 0
)

invalid_order_id = (
    df["order_id"] <= 0
)


invalid_value_rows = (
    invalid_quantity
    | invalid_price
    | invalid_order_id
)


invalid_count = int(
    invalid_value_rows.sum()
)


if invalid_count > 0:

    print(
        "Invalid value rows removed:",
        invalid_count
    )

    df = df[
        ~invalid_value_rows
    ].copy()


# ==========================================
# CONVERT INTEGER COLUMNS
# ==========================================

df["order_id"] = (
    df["order_id"]
    .astype("int64")
)

df["quantity"] = (
    df["quantity"]
    .astype("int64")
)

df["price"] = (
    df["price"]
    .astype("int64")
)


# ==========================================
# FORMAT DATE
# ==========================================

df["order_date"] = (
    df["order_date"]
    .dt.strftime("%Y-%m-%d")
)


# ==========================================
# CALCULATE TOTAL SALES
# ==========================================

df["total_sales"] = (
    df["quantity"]
    * df["price"]
)


# ==========================================
# FINAL COLUMN ORDER
# ==========================================

df = df[
    [
        "order_id",
        "order_date",
        "product",
        "category",
        "quantity",
        "price",
        "city",
        "total_sales"
    ]
]


# ==========================================
# FINAL DUPLICATE ORDER CHECK
# ==========================================

duplicate_order_ids = (
    df["order_id"].duplicated()
)

duplicate_order_count = int(
    duplicate_order_ids.sum()
)


if duplicate_order_count > 0:

    print(
        "\n❌ ERROR: Duplicate order IDs detected "
        "after cleaning."
    )

    print(
        "Duplicate count:",
        duplicate_order_count
    )

    sys.exit(1)


# ==========================================
# CHECK FINAL DATA
# ==========================================

if df.empty:

    fail(
        "No valid rows remain after cleaning."
    )


# ==========================================
# DISPLAY CLEANED DATA
# ==========================================

print("\nCleaned data:")
print(df)

print("\nFinal rows:", len(df))


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

CLEANED_DATA_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# SAVE CLEANED DATA
# ==========================================

try:

    df.to_csv(
        CLEANED_DATA_FILE,
        index=False
    )

except Exception as error:

    fail(
        f"Could not save cleaned data: {error}"
    )


print(
    "\nCleaned data saved to:",
    CLEANED_DATA_FILE
)