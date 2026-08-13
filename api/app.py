import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
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
def get_sales():

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
        ORDER BY order_date, order_id;
    """

    df = pd.read_sql_query(
        query,
        engine
    )

    df["order_date"] = df[
        "order_date"
    ].astype(str)

    return df.to_dict(
        orient="records"
    )