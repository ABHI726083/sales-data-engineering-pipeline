import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Sales Data Engineering API",
    description="API for the Sales Data Engineering Pipeline",
    version="1.0.0",
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection_url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(connection_url)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Sales Data Engineering API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# SALES ENDPOINT
# ============================================================

@app.get("/sales")
def get_sales(
    city: str | None = Query(default=None),
    category: str | None = Query(default=None),
    product: str | None = Query(default=None),
):

    engine = get_connection()

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
        WHERE (%(city)s IS NULL OR city = %(city)s)
          AND (%(category)s IS NULL OR category = %(category)s)
          AND (%(product)s IS NULL OR product = %(product)s)
        ORDER BY order_date, order_id;
    """

    df = pd.read_sql_query(
        query,
        engine,
        params={
            "city": city,
            "category": category,
            "product": product,
        }
    )

    df["order_date"] = df[
        "order_date"
    ].astype(str)

    return df.to_dict(
        orient="records"
    )


# ============================================================
# ANALYTICS SUMMARY
# ============================================================

@app.get("/analytics/summary")
def get_summary():

    engine = get_connection()

    query = """
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(quantity), 0) AS total_quantity,
            COALESCE(SUM(total_sales), 0) AS total_sales,
            COALESCE(AVG(total_sales), 0) AS average_order_value
        FROM sales;
    """

    df = pd.read_sql_query(
        query,
        engine
    )

    result = df.iloc[0].to_dict()

    return {
        "total_orders": int(result["total_orders"]),
        "total_quantity": int(result["total_quantity"]),
        "total_sales": float(result["total_sales"]),
        "average_order_value": float(
            result["average_order_value"]
        ),
    }


# ============================================================
# SALES BY CITY
# ============================================================

@app.get("/analytics/city")
def get_sales_by_city():

    engine = get_connection()

    query = """
        SELECT
            city,
            COALESCE(SUM(total_sales), 0) AS total_sales
        FROM sales
        GROUP BY city
        ORDER BY total_sales DESC;
    """

    df = pd.read_sql_query(
        query,
        engine
    )

    return df.to_dict(
        orient="records"
    )


# ============================================================
# SALES BY CATEGORY
# ============================================================

@app.get("/analytics/category")
def get_sales_by_category():

    engine = get_connection()

    query = """
        SELECT
            category,
            COALESCE(SUM(total_sales), 0) AS total_sales
        FROM sales
        GROUP BY category
        ORDER BY total_sales DESC;
    """

    df = pd.read_sql_query(
        query,
        engine
    )

    return df.to_dict(
        orient="records"
    )


# ============================================================
# SALES BY PRODUCT
# ============================================================

@app.get("/analytics/product")
def get_sales_by_product():

    engine = get_connection()

    query = """
        SELECT
            product,
            COALESCE(SUM(total_sales), 0) AS total_sales
        FROM sales
        GROUP BY product
        ORDER BY total_sales DESC;
    """

    df = pd.read_sql_query(
        query,
        engine
    )

    return df.to_dict(
        orient="records"
    )