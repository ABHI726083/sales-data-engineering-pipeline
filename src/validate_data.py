import sys
import pandas as pd

# ==========================================
# FORCE UTF-8 OUTPUT
# ==========================================

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


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
    "city",
    "total_sales"
]


# ==========================================
# PRINT ERROR AND EXIT
# ==========================================

def fail(message):
    print(f"\n❌ ERROR: {message}")
    sys.exit(1)


# ==========================================
# CHECK INPUT FILE ARGUMENT
# ==========================================

if len(sys.argv) < 2:

    print("ERROR: Please provide a CSV file path.")
    print("Example:")
    print("python validate_data.py output/cleaned_sales.csv")

    sys.exit(1)


# ==========================================
# GET INPUT FILE
# ==========================================

file_path = sys.argv[1]

print("Validation input file:", file_path)


# ==========================================
# LOAD DATA
# ==========================================

try:

    df = pd.read_csv(file_path)

except FileNotFoundError:

    print("ERROR: Validation file not found!")
    print("File:", file_path)

    sys.exit(1)

except pd.errors.EmptyDataError:

    print("ERROR: Validation CSV file is empty.")
    sys.exit(1)

except pd.errors.ParserError as error:

    print("ERROR: Could not parse validation CSV.")
    print(error)

    sys.exit(1)

except Exception as error:

    print("ERROR: Could not read validation CSV.")
    print(error)

    sys.exit(1)


# ==========================================
# BASIC INFORMATION
# ==========================================

print("\nStarting data validation...")

print("Rows:", len(df))


# ==========================================
# CHECK EMPTY DATASET
# ==========================================

if df.empty:

    print("\n❌ VALIDATION FAILED")
    print("CSV contains no data rows.")

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

if missing_columns:

    print("\n❌ DATA SCHEMA ERROR")

    print("Missing columns:")

    for column in missing_columns:
        print("-", column)

    sys.exit(1)


print("Required columns: OK")


# ==========================================
# CHECK MISSING VALUES
# ==========================================

print("\nMissing values:")

missing_values = df[REQUIRED_COLUMNS].isnull().sum()

print(missing_values)

missing_value_count = int(
    missing_values.sum()
)

if missing_value_count > 0:

    print("\n❌ VALIDATION FAILED")
    print("Missing values detected.")

    sys.exit(1)


# ==========================================
# CHECK DUPLICATE ORDER IDs
# ==========================================

duplicate_order_ids = int(
    df["order_id"].duplicated().sum()
)

print(
    "\nDuplicate order IDs:",
    duplicate_order_ids
)

if duplicate_order_ids > 0:

    print("\n❌ VALIDATION FAILED")
    print("Duplicate order IDs detected.")

    sys.exit(1)


# ==========================================
# CHECK DUPLICATE ROWS
# ==========================================

duplicate_rows = int(
    df.duplicated().sum()
)

print(
    "Duplicate rows:",
    duplicate_rows
)

if duplicate_rows > 0:

    print("\n❌ VALIDATION FAILED")
    print("Duplicate rows detected.")

    sys.exit(1)


# ==========================================
# CHECK ORDER ID
# ==========================================

order_id_numeric = pd.to_numeric(
    df["order_id"],
    errors="coerce"
)

invalid_order_id = int(
    (
        order_id_numeric.isnull()
        | (order_id_numeric <= 0)
        | (order_id_numeric % 1 != 0)
    ).sum()
)

print(
    "\nInvalid order IDs:",
    invalid_order_id
)

if invalid_order_id > 0:

    print("\n❌ VALIDATION FAILED")
    print(
        "Order IDs must be positive integers."
    )

    sys.exit(1)


# ==========================================
# CHECK DATE
# ==========================================

dates = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

invalid_dates = int(
    dates.isnull().sum()
)

print(
    "Invalid dates:",
    invalid_dates
)

if invalid_dates > 0:

    print("\n❌ VALIDATION FAILED")
    print("Invalid order dates detected.")

    sys.exit(1)


# ==========================================
# CHECK QUANTITY
# ==========================================

quantity_numeric = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

invalid_quantity = int(
    (
        quantity_numeric.isnull()
        | (quantity_numeric <= 0)
        | (quantity_numeric % 1 != 0)
    ).sum()
)

print(
    "Invalid quantity:",
    invalid_quantity
)

if invalid_quantity > 0:

    print("\n❌ VALIDATION FAILED")
    print(
        "Quantity must be a positive integer."
    )

    sys.exit(1)


# ==========================================
# CHECK PRICE
# ==========================================

price_numeric = pd.to_numeric(
    df["price"],
    errors="coerce"
)

invalid_price = int(
    (
        price_numeric.isnull()
        | (price_numeric < 0)
    ).sum()
)

print(
    "Invalid price:",
    invalid_price
)

if invalid_price > 0:

    print("\n❌ VALIDATION FAILED")
    print(
        "Price must be a non-negative number."
    )

    sys.exit(1)


# ==========================================
# CHECK TOTAL SALES
# ==========================================

total_sales_numeric = pd.to_numeric(
    df["total_sales"],
    errors="coerce"
)

expected_total_sales = (
    quantity_numeric * price_numeric
)

invalid_total_sales = int(
    (
        total_sales_numeric.isnull()
        | (
            total_sales_numeric
            != expected_total_sales
        )
    ).sum()
)

print(
    "Invalid total sales:",
    invalid_total_sales
)

if invalid_total_sales > 0:

    print("\n❌ VALIDATION FAILED")
    print(
        "total_sales does not match "
        "quantity × price."
    )

    sys.exit(1)


# ==========================================
# CHECK TEXT COLUMNS
# ==========================================

text_columns = [
    "product",
    "category",
    "city"
]

invalid_text = 0

for column in text_columns:

    invalid_count = int(
        df[column]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    if invalid_count > 0:

        print(
            f"Invalid {column}: "
            f"{invalid_count}"
        )

        invalid_text += invalid_count


if invalid_text > 0:

    print("\n❌ VALIDATION FAILED")
    print("Blank text values detected.")

    sys.exit(1)


# ==========================================
# CHECK TEXT VALUES FOR NULL AFTER CLEANING
# ==========================================

null_text_values = 0

for column in text_columns:

    null_count = int(
        df[column].isnull().sum()
    )

    null_text_values += null_count


if null_text_values > 0:

    print("\n❌ VALIDATION FAILED")
    print("Missing text values detected.")

    sys.exit(1)


# ==========================================
# DATA QUALITY SUMMARY
# ==========================================

print("\n================================")
print("DATA QUALITY SUMMARY")
print("================================")

print("Required columns: OK")
print(
    "Missing values:",
    missing_value_count
)
print(
    "Duplicate order IDs:",
    duplicate_order_ids
)
print(
    "Duplicate rows:",
    duplicate_rows
)
print(
    "Invalid order IDs:",
    invalid_order_id
)
print(
    "Invalid dates:",
    invalid_dates
)
print(
    "Invalid quantity:",
    invalid_quantity
)
print(
    "Invalid price:",
    invalid_price
)
print(
    "Invalid total sales:",
    invalid_total_sales
)
print("Text fields: OK")


# ==========================================
# VALIDATION SUCCESS
# ==========================================

print("\n✅ DATA VALIDATION PASSED!")

sys.exit(0)