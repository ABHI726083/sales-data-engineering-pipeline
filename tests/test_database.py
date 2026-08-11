import sys
from pathlib import Path

import pandas as pd
import pytest


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    import psycopg2

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


# ============================================================
# DATABASE AVAILABILITY
# ============================================================

@pytest.fixture
def db_connection():

    try:

        conn = get_connection()

    except Exception as error:

        pytest.skip(
            f"PostgreSQL is not available: {error}"
        )

    yield conn

    conn.close()


# ============================================================
# TEST 1: DATABASE CONNECTION
# ============================================================

def test_database_connection(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT 1;"
    )

    result = cursor.fetchone()

    cursor.close()

    assert result[0] == 1


# ============================================================
# TEST 2: SALES TABLE EXISTS
# ============================================================

def test_sales_table_exists(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'sales'
        );
        """
    )

    exists = cursor.fetchone()[0]

    cursor.close()

    assert exists is True


# ============================================================
# TEST 3: DATABASE ROW COUNT
# ============================================================

def test_sales_table_has_data(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales;
        """
    )

    row_count = cursor.fetchone()[0]

    cursor.close()

    assert row_count > 0


# ============================================================
# TEST 4: REQUIRED COLUMNS EXIST
# ============================================================

def test_sales_table_columns(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'sales'
        ORDER BY ordinal_position;
        """
    )

    columns = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()

    expected_columns = [
        "order_id",
        "order_date",
        "product",
        "category",
        "quantity",
        "price",
        "city",
        "total_sales",
    ]

    assert columns == expected_columns


# ============================================================
# TEST 5: ORDER ID IS UNIQUE
# ============================================================

def test_order_ids_are_unique(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(order_id),
            COUNT(DISTINCT order_id)
        FROM sales;
        """
    )

    total_ids, unique_ids = (
        cursor.fetchone()
    )

    cursor.close()

    assert total_ids == unique_ids


# ============================================================
# TEST 6: TOTAL SALES CALCULATION
# ============================================================

def test_total_sales_calculation(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*)
        FROM sales
        WHERE total_sales != quantity * price;
        """
    )

    invalid_rows = cursor.fetchone()[0]

    cursor.close()

    assert invalid_rows == 0


# ============================================================
# TEST 7: QUANTITY MUST BE POSITIVE
# ============================================================

def test_quantity_is_positive(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales
        WHERE quantity <= 0;
        """
    )

    invalid_rows = cursor.fetchone()[0]

    cursor.close()

    assert invalid_rows == 0


# ============================================================
# TEST 8: PRICE MUST BE NON-NEGATIVE
# ============================================================

def test_price_is_valid(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales
        WHERE price < 0;
        """
    )

    invalid_rows = cursor.fetchone()[0]

    cursor.close()

    assert invalid_rows == 0


# ============================================================
# TEST 9: TOTAL SALES MATCHES PIPELINE DATA
# ============================================================

def test_total_sales_value(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(total_sales), 0)
        FROM sales;
        """
    )

    total_sales = cursor.fetchone()[0]

    cursor.close()

    assert total_sales == 301500


# ============================================================
# TEST 10: TOTAL QUANTITY
# ============================================================

def test_total_quantity(
    db_connection
):

    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(quantity), 0)
        FROM sales;
        """
    )

    total_quantity = cursor.fetchone()[0]

    cursor.close()

    assert total_quantity == 41