import os
from io import StringIO

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_sales_data():
    conn = get_connection()

    query = """
        SELECT
            order_id,
            order_date,
            product,
            category,
            quantity,
            price,
            city,
            total_sales
        FROM sales
        ORDER BY order_date, order_id;
    """

    df = pd.read_sql_query(query, conn)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    ).dt.date

    return df


# ============================================================
# LOAD DATABASE DATA
# ============================================================

try:
    df = load_sales_data()

except Exception as error:

    st.error(
        "Unable to connect to PostgreSQL or load sales data."
    )

    st.exception(error)

    st.stop()


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("📊 Sales Analytics Dashboard")

st.caption(
    "Interactive sales analytics powered by PostgreSQL"
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")


# ----------------------------
# City Filter
# ----------------------------

cities = sorted(
    df["city"].dropna().unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "City",
    ["All Cities"] + cities
)


# ----------------------------
# Category Filter
# ----------------------------

categories = sorted(
    df["category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All Categories"] + categories
)


# ----------------------------
# Date Filter
# ----------------------------

min_date = df["order_date"].min()
max_date = df["order_date"].max()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ============================================================
# HANDLE DATE RANGE
# ============================================================

if isinstance(selected_dates, tuple):

    if len(selected_dates) == 2:

        start_date, end_date = selected_dates

    else:

        start_date = min_date
        end_date = max_date

else:

    start_date = selected_dates
    end_date = selected_dates


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


if selected_city != "All Cities":

    filtered_df = filtered_df[
        filtered_df["city"] == selected_city
    ]


if selected_category != "All Categories":

    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]


filtered_df = filtered_df[
    (filtered_df["order_date"] >= start_date)
    &
    (filtered_df["order_date"] <= end_date)
]


# ============================================================
# FILTER SUMMARY
# ============================================================

st.sidebar.divider()

st.sidebar.write(
    f"Filtered rows: **{len(filtered_df)}**"
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["total_sales"].sum()

total_quantity = filtered_df["quantity"].sum()

total_orders = filtered_df["order_id"].nunique()


if total_orders > 0:

    average_order_value = (
        total_sales / total_orders
    )

else:

    average_order_value = 0


# ============================================================
# TOP PRODUCT
# ============================================================

if not filtered_df.empty:

    product_sales = (
        filtered_df
        .groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_sales.index[0]

else:

    top_product = "N/A"


# ============================================================
# TOP CITY
# ============================================================

if not filtered_df.empty:

    city_sales = (
        filtered_df
        .groupby("city")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_city = city_sales.index[0]

else:

    top_city = "N/A"


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)


col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)


col3.metric(
    "Total Quantity",
    f"{total_quantity:,}"
)


col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)


# ============================================================
# SECONDARY KPIs
# ============================================================

col5, col6 = st.columns(2)


col5.metric(
    "Top Product",
    top_product
)


col6.metric(
    "Top City",
    top_city
)


# ============================================================
# NO DATA MESSAGE
# ============================================================

if filtered_df.empty:

    st.warning(
        "No sales data matches the selected filters."
    )

    st.stop()


# ============================================================
# SALES BY CITY
# ============================================================

st.subheader("Sales by City")

sales_by_city = (
    filtered_df
    .groupby("city")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(
    sales_by_city
)


# ============================================================
# SALES BY CATEGORY
# ============================================================

st.subheader("Sales by Category")

sales_by_category = (
    filtered_df
    .groupby("category")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(
    sales_by_category
)


# ============================================================
# SALES BY PRODUCT
# ============================================================

st.subheader("Sales by Product")

sales_by_product = (
    filtered_df
    .groupby("product")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(
    sales_by_product
)


# ============================================================
# DAILY SALES TREND
# ============================================================

st.subheader("Daily Sales Trend")

daily_sales = (
    filtered_df
    .groupby("order_date")["total_sales"]
    .sum()
    .sort_index()
)

st.line_chart(
    daily_sales
)


# ============================================================
# QUANTITY BY PRODUCT
# ============================================================

st.subheader("Quantity Sold by Product")

quantity_by_product = (
    filtered_df
    .groupby("product")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(
    quantity_by_product
)


# ============================================================
# FILTERED DATA
# ============================================================

st.subheader("Filtered Sales Data")

display_df = filtered_df.copy()

display_df["order_date"] = display_df[
    "order_date"
].astype(str)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv_buffer = StringIO()

display_df.to_csv(
    csv_buffer,
    index=False
)

st.download_button(
    label="Download Filtered Data",
    data=csv_buffer.getvalue(),
    file_name="filtered_sales.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Data source: PostgreSQL | "
    "Data pipeline: Python + Pandas + PostgreSQL + Streamlit"
)