import requests
import pandas as pd
import streamlit as st
from io import StringIO
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

API_URL = "http://127.0.0.1:8000"


# ============================================================
# LOAD DATA FROM FASTAPI
# ============================================================

@st.cache_data
def load_sales_data():

    response = requests.get(
        f"{API_URL}/sales",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    ).dt.date

    return df


# ============================================================
# LOAD SALES DATA
# ============================================================

try:

    df = load_sales_data()

except requests.exceptions.ConnectionError:

    st.error(
        "Unable to connect to FastAPI. "
        "Make sure Uvicorn is running on http://127.0.0.1:8000"
    )

    st.stop()

except requests.exceptions.RequestException as error:

    st.error(
        "FastAPI returned an error while loading sales data."
    )

    st.exception(error)

    st.stop()

except Exception as error:

    st.error(
        "Unable to load sales data."
    )

    st.exception(error)

    st.stop()


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("📊 Sales Analytics Dashboard")

st.caption(
    "Interactive sales analytics powered by FastAPI + PostgreSQL"
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")


# ============================================================
# CITY FILTER
# ============================================================

cities = sorted(
    df["city"].dropna().unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "City",
    ["All Cities"] + cities
)


# ============================================================
# CATEGORY FILTER
# ============================================================

categories = sorted(
    df["category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All Categories"] + categories
)


# ============================================================
# PRODUCT FILTER
# ============================================================

products = sorted(
    df["product"].dropna().unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "Product",
    ["All Products"] + products
)


# ============================================================
# DATE FILTER
# ============================================================

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


if selected_product != "All Products":

    filtered_df = filtered_df[
        filtered_df["product"] == selected_product
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

summary_response = requests.get(
    f"{API_URL}/analytics/summary",
    timeout=10
)

summary_response.raise_for_status()

summary = summary_response.json()


# ============================================================
# FILTERED KPI CALCULATIONS
# ============================================================

if (
    selected_city == "All Cities"
    and selected_category == "All Categories"
    and selected_product == "All Products"
    and start_date == min_date
    and end_date == max_date
):

    total_sales = summary["total_sales"]

    total_quantity = summary["total_quantity"]

    total_orders = summary["total_orders"]

    average_order_value = summary[
        "average_order_value"
    ]

else:

    total_sales = filtered_df[
        "total_sales"
    ].sum()

    total_quantity = filtered_df[
        "quantity"
    ].sum()

    total_orders = filtered_df[
        "order_id"
    ].nunique()

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
# CHECK WHETHER DASHBOARD IS UNFILTERED
# ============================================================

is_unfiltered = (
    selected_city == "All Cities"
    and selected_category == "All Categories"
    and selected_product == "All Products"
    and start_date == min_date
    and end_date == max_date
)


# ============================================================
# SALES BY CITY
# ============================================================

st.subheader("Sales by City")


if is_unfiltered:

    city_response = requests.get(
        f"{API_URL}/analytics/city",
        timeout=10
    )

    city_response.raise_for_status()

    city_data = city_response.json()

    city_df = pd.DataFrame(city_data)

    sales_by_city = city_df.set_index(
        "city"
    )["total_sales"]

else:

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


if is_unfiltered:

    category_response = requests.get(
        f"{API_URL}/analytics/category",
        timeout=10
    )

    category_response.raise_for_status()

    category_data = category_response.json()

    category_df = pd.DataFrame(
        category_data
    )

    sales_by_category = category_df.set_index(
        "category"
    )["total_sales"]

else:

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


if is_unfiltered:

    product_response = requests.get(
        f"{API_URL}/analytics/product",
        timeout=10
    )

    product_response.raise_for_status()

    product_data = product_response.json()

    product_df = pd.DataFrame(
        product_data
    )

    sales_by_product = product_df.set_index(
        "product"
    )["total_sales"]

else:

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
    width="stretch",
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
    "API: FastAPI | "
    "Dashboard: Streamlit | "
    "Pipeline: Python + Pandas"
)