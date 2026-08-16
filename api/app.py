import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

connection_url = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Sales Data Engineering API",
    description="API for the Sales Data Engineering Pipeline",
    version="1.0.0",
)


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

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "healthy",
            "database": "connected"
        }

    except SQLAlchemyError:

        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )


# ============================================================
# SALES ENDPOINT
# ============================================================

@app.get("/sales")
def get_sales(
    city: str | None = Query(default=None),
    category: str | None = Query(default=None),
    product: str | None = Query(default=None),
    limit: int = Query(
        default=100,
        ge=1,
        le=1000
    ),
    offset: int = Query(
        default=0,
        ge=0
    ),
):

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
        ORDER BY order_date, order_id
        LIMIT %(limit)s
        OFFSET %(offset)s;
    """

    try:

        df = pd.read_sql_query(
            query,
            engine,
            params={
                "city": city,
                "category": category,
                "product": product,
                "limit": limit,
                "offset": offset,
            }
        )

        df["order_date"] = df[
            "order_date"
        ].astype(str)

        return df.to_dict(
            orient="records"
        )

    except SQLAlchemyError:

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve sales data"
        )


# ============================================================
# ANALYTICS SUMMARY
# ============================================================

@app.get("/analytics/summary")
def get_summary():

    query = """
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(quantity), 0) AS total_quantity,
            COALESCE(SUM(total_sales), 0) AS total_sales,
            COALESCE(AVG(total_sales), 0) AS average_order_value
        FROM sales;
    """

    try:

        df = pd.read_sql_query(
            query,
            engine
        )

        result = df.iloc[0].to_dict()

        return {
            "total_orders": int(
                result["total_orders"]
            ),
            "total_quantity": int(
                result["total_quantity"]
            ),
            "total_sales": float(
                result["total_sales"]
            ),
            "average_order_value": float(
                result["average_order_value"]
            ),
        }

    except SQLAlchemyError:

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve summary analytics"
        )


# ============================================================
# SALES BY CITY
# ============================================================

@app.get("/analytics/city")
def get_sales_by_city():

    query = """
        SELECT
            city,
            COALESCE(SUM(total_sales), 0) AS total_sales
        FROM sales
        GROUP BY city
        ORDER BY total_sales DESC;
    """

    try:

        df = pd.read_sql_query(
            query,
            engine
        )

        return df.to_dict(
            orient="records"
        )

    except SQLAlchemyError:

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve city analytics"
        )


# ============================================================
# SALES BY CATEGORY
# ============================================================

@app.get("/analytics/category")
def get_sales_by_category():

    query = """
        SELECT
            category,
            COALESCE(SUM(total_sales), 0) AS total_sales
        FROM sales
        GROUP BY category
        ORDER BY total_sales DESC;
    """

    try:

        df = pd.read_sql_query(
            query,
            engine
        )

        return df.to_dict(
            orient="records"
        )

    except SQLAlchemyError:

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve category analytics"
        )


# ============================================================
# SALES BY PRODUCT
# ============================================================

@app.get("/analytics/product")
def get_sales_by_product():

    query = """
        SELECT
            product,
            COALESCE(SUM(total_sales), 0) AS total_sales
        FROM sales
        GROUP BY product
        ORDER BY total_sales DESC;
    """

    try:

        df = pd.read_sql_query(
            query,
            engine
        )

        return df.to_dict(
            orient="records"
        )

    except SQLAlchemyError:

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve product analytics"
        )