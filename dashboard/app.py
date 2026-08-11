import os
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Connect to PostgreSQL
# -----------------------------

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

# -----------------------------
# Dashboard Title
# -----------------------------

st.title("Sales Analytics Dashboard")

# -----------------------------
# Filters
# -----------------------------

# City Filter
cursor.execute("""
SELECT DISTINCT city
FROM sales
ORDER BY city;
""")

cities = [row[0] for row in cursor.fetchall()]

selected_city = st.selectbox(
    "Select City",
    ["All Cities"] + cities
)

# Date Filter
cursor.execute("""
SELECT MIN(order_date), MAX(order_date)
FROM sales;
""")

min_date, max_date = cursor.fetchone()

start_date, end_date = st.date_input(
    "Select Date Range",
    value=(min_date, max_date)
)

# -----------------------------
# Build SQL Filter
# -----------------------------

conditions = []
params = []

if selected_city != "All Cities":
    conditions.append("city = %s")
    params.append(selected_city)

conditions.append("order_date BETWEEN %s AND %s")
params.append(start_date)
params.append(end_date)

where_clause = "WHERE " + " AND ".join(conditions)

# -----------------------------
# Total Sales
# -----------------------------

cursor.execute(f"""
SELECT SUM(total_sales)
FROM sales
{where_clause};
""", tuple(params))

total_sales = cursor.fetchone()[0] or 0

# -----------------------------
# Total Quantity
# -----------------------------

cursor.execute(f"""
SELECT SUM(quantity)
FROM sales
{where_clause};
""", tuple(params))

total_quantity = cursor.fetchone()[0] or 0

# -----------------------------
# Top Product
# -----------------------------

cursor.execute(f"""
SELECT product, SUM(total_sales) AS total_sales
FROM sales
{where_clause}
GROUP BY product
ORDER BY total_sales DESC
LIMIT 1;
""", tuple(params))

top_product_result = cursor.fetchone()

if top_product_result:
    top_product = top_product_result[0]
else:
    top_product = "N/A"

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,}"
)

col2.metric(
    "Total Quantity",
    total_quantity
)

col3.metric(
    "Top Product",
    top_product
)

# -----------------------------
# Sales by City
# -----------------------------

cursor.execute(f"""
SELECT city, SUM(total_sales) AS total_sales
FROM sales
{where_clause}
GROUP BY city
ORDER BY total_sales DESC;
""", tuple(params))

city_results = cursor.fetchall()

city_data = {
    "City": [row[0] for row in city_results],
    "Sales": [row[1] for row in city_results]
}

st.subheader("Sales by City")

st.bar_chart(
    city_data,
    x="City",
    y="Sales"
)

# -----------------------------
# Sales by Category
# -----------------------------

cursor.execute(f"""
SELECT category, SUM(total_sales) AS total_sales
FROM sales
{where_clause}
GROUP BY category
ORDER BY total_sales DESC;
""", tuple(params))

category_results = cursor.fetchall()

category_data = {
    "Category": [row[0] for row in category_results],
    "Sales": [row[1] for row in category_results]
}

st.subheader("Sales by Category")

st.bar_chart(
    category_data,
    x="Category",
    y="Sales"
)

# -----------------------------
# Sales by Product
# -----------------------------

cursor.execute(f"""
SELECT product, SUM(total_sales) AS total_sales
FROM sales
{where_clause}
GROUP BY product
ORDER BY total_sales DESC;
""", tuple(params))

product_results = cursor.fetchall()

product_data = {
    "Product": [row[0] for row in product_results],
    "Sales": [row[1] for row in product_results]
}

st.subheader("Sales by Product")

st.bar_chart(
    product_data,
    x="Product",
    y="Sales"
)

# -----------------------------
# Close Database
# -----------------------------

cursor.close()
conn.close()