import os
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================

INPUT_FILE = "output/cleaned_sales.csv"
OUTPUT_DIR = "output/reports"

# Create reports folder
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# LOAD CLEANED DATA
# ==========================================

print("Loading cleaned data...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")


# ==========================================
# REPORT 1: SALES BY CITY
# ==========================================

sales_by_city = (
    df.groupby("city", as_index=False)["total_sales"]
    .sum()
    .sort_values("total_sales", ascending=False)
)

sales_by_city.to_csv(
    f"{OUTPUT_DIR}/sales_by_city.csv",
    index=False
)

print("Sales by city report created.")


# ==========================================
# REPORT 2: SALES BY CATEGORY
# ==========================================

sales_by_category = (
    df.groupby("category", as_index=False)["total_sales"]
    .sum()
    .sort_values("total_sales", ascending=False)
)

sales_by_category.to_csv(
    f"{OUTPUT_DIR}/sales_by_category.csv",
    index=False
)

print("Sales by category report created.")


# ==========================================
# REPORT 3: SALES BY PRODUCT
# ==========================================

sales_by_product = (
    df.groupby("product", as_index=False)["total_sales"]
    .sum()
    .sort_values("total_sales", ascending=False)
)

sales_by_product.to_csv(
    f"{OUTPUT_DIR}/sales_by_product.csv",
    index=False
)

print("Sales by product report created.")


# ==========================================
# REPORT 4: QUANTITY BY PRODUCT
# ==========================================

quantity_by_product = (
    df.groupby("product", as_index=False)["quantity"]
    .sum()
    .sort_values("quantity", ascending=False)
)

quantity_by_product.to_csv(
    f"{OUTPUT_DIR}/quantity_by_product.csv",
    index=False
)

print("Quantity by product report created.")


# ==========================================
# PIPELINE SUMMARY
# ==========================================

total_sales = df["total_sales"].sum()
total_quantity = df["quantity"].sum()
total_orders = df["order_id"].nunique()

summary = pd.DataFrame({
    "metric": [
        "Total Orders",
        "Total Quantity Sold",
        "Total Sales"
    ],
    "value": [
        total_orders,
        total_quantity,
        total_sales
    ]
})

summary.to_csv(
    f"{OUTPUT_DIR}/pipeline_summary.csv",
    index=False
)

print("Pipeline summary report created.")


# ==========================================
# COMPLETE
# ==========================================

print()
print("=" * 40)
print("REPORT GENERATION COMPLETED")
print("=" * 40)

print(f"Reports saved to: {OUTPUT_DIR}")