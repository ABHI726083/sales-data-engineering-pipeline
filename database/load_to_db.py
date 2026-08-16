import sys
from pathlib import Path

import pandas as pd
import psycopg2

from config.settings import (
    CLEANED_DATA_FILE,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

from utils.logger import (
    log_info,
    log_warning,
    log_error,
    log_exception,
)


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# UTF-8 OUTPUT
# ============================================================

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(
        encoding="utf-8"
    )

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(
        encoding="utf-8"
    )


# ============================================================
# HELPER
# ============================================================

def fail(message):

    print(
        f"\nERROR: {message}"
    )

    log_error(message)

    sys.exit(1)


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = None
cursor = None


try:

    # ========================================================
    # STEP 1: LOAD CLEANED DATA
    # ========================================================

    print("\n================================")
    print("LOAD CLEANED DATA")
    print("================================")

    log_info(
        "STEP 1: LOAD CLEANED DATA"
    )

    cleaned_file = Path(
        CLEANED_DATA_FILE
    )

    if not cleaned_file.is_absolute():

        cleaned_file = (
            PROJECT_ROOT / cleaned_file
        )

    if not cleaned_file.is_file():

        fail(
            f"Cleaned data file not found: "
            f"{cleaned_file}"
        )

    df = pd.read_csv(
        cleaned_file
    )

    if df.empty:

        fail(
            "Cleaned data file contains no rows."
        )

    required_columns = [
        "order_id",
        "order_date",
        "product",
        "category",
        "quantity",
        "price",
        "city",
        "total_sales",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        fail(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="raise"
    ).dt.date

    print(
        "Cleaned data loaded!"
    )

    print(
        "Rows:",
        len(df)
    )

    log_info(
        f"Cleaned data loaded successfully - "
        f"rows={len(df)}"
    )


    # ========================================================
    # STEP 2: CONNECT TO POSTGRESQL
    # ========================================================

    print("\n================================")
    print("CONNECT TO POSTGRESQL")
    print("================================")

    log_info(
        "STEP 2: CONNECT TO POSTGRESQL"
    )

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cursor = conn.cursor()

    print(
        "Connected to PostgreSQL successfully!"
    )

    log_info(
        "Connected to PostgreSQL successfully"
    )


    # ========================================================
    # STEP 3: CREATE TABLE
    # ========================================================

    print("\n================================")
    print("PREPARE DATABASE TABLE")
    print("================================")

    log_info(
        "STEP 3: PREPARE DATABASE TABLE"
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            order_id INTEGER PRIMARY KEY,
            order_date DATE NOT NULL,
            product VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL,
            city VARCHAR(100) NOT NULL,
            total_sales INTEGER NOT NULL
        );
        """
    )

    print(
        "Sales table ready."
    )

    log_info(
        "Sales table ready"
    )


    # ========================================================
    # STEP 4: UPSERT DATA
    # ========================================================

    print("\n================================")
    print("UPSERT DATA")
    print("================================")

    log_info(
        "STEP 4: UPSERT DATA"
    )

    inserted = 0
    updated = 0
    unchanged = 0


    for _, row in df.iterrows():

        order_id = int(
            row["order_id"]
        )


        # ====================================================
        # CHECK EXISTING ORDER
        # ====================================================

        cursor.execute(
            """
            SELECT
                order_date,
                product,
                category,
                quantity,
                price,
                city,
                total_sales
            FROM sales
            WHERE order_id = %s;
            """,
            (order_id,)
        )

        existing_row = cursor.fetchone()


        # ====================================================
        # NEW ORDER
        # ====================================================

        if existing_row is None:

            cursor.execute(
                """
                INSERT INTO sales (
                    order_id,
                    order_date,
                    product,
                    category,
                    quantity,
                    price,
                    city,
                    total_sales
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                );
                """,
                (
                    order_id,
                    row["order_date"],
                    row["product"],
                    row["category"],
                    int(row["quantity"]),
                    int(row["price"]),
                    row["city"],
                    int(row["total_sales"]),
                )
            )

            inserted += 1

            print(
                f"Inserted new order: {order_id}"
            )

            continue


        # ====================================================
        # EXISTING ORDER VALUES
        # ====================================================

        old_values = (
            existing_row[0],
            existing_row[1],
            existing_row[2],
            int(existing_row[3]),
            int(existing_row[4]),
            existing_row[5],
            int(existing_row[6]),
        )

        new_values = (
            row["order_date"],
            row["product"],
            row["category"],
            int(row["quantity"]),
            int(row["price"]),
            row["city"],
            int(row["total_sales"]),
        )


        # ====================================================
        # UNCHANGED
        # ====================================================

        if old_values == new_values:

            unchanged += 1

            print(
                f"Unchanged order: {order_id}"
            )

            continue


        # ====================================================
        # UPDATE CHANGED ORDER
        # ====================================================

        cursor.execute(
            """
            UPDATE sales
            SET
                order_date = %s,
                product = %s,
                category = %s,
                quantity = %s,
                price = %s,
                city = %s,
                total_sales = %s
            WHERE order_id = %s;
            """,
            (
                row["order_date"],
                row["product"],
                row["category"],
                int(row["quantity"]),
                int(row["price"]),
                row["city"],
                int(row["total_sales"]),
                order_id,
            )
        )

        updated += 1

        print(
            f"Updated existing order: {order_id}"
        )


    # ========================================================
    # STEP 5: COMMIT TRANSACTION
    # ========================================================

    print("\n================================")
    print("COMMIT TRANSACTION")
    print("================================")

    log_info(
        "STEP 5: COMMIT TRANSACTION"
    )

    conn.commit()

    print(
        "Database transaction committed successfully!"
    )

    log_info(
        "Database transaction committed successfully"
    )


    # ========================================================
    # STEP 6: LOADING SUMMARY
    # ========================================================

    print("\n================================")
    print("LOADING SUMMARY")
    print("================================")

    print(
        "New rows inserted:",
        inserted
    )

    print(
        "Existing rows updated:",
        updated
    )

    print(
        "Unchanged rows:",
        unchanged
    )

    log_info(
        f"Loading summary - "
        f"inserted={inserted}, "
        f"updated={updated}, "
        f"unchanged={unchanged}"
    )


    # ========================================================
    # STEP 7: VERIFY DATABASE
    # ========================================================

    print("\n================================")
    print("VERIFY DATABASE")
    print("================================")

    log_info(
        "STEP 7: VERIFY DATABASE"
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales;
        """
    )

    row_count = cursor.fetchone()[0]

    print(
        "Rows in PostgreSQL:",
        row_count
    )


    # ========================================================
    # VERIFY EXPECTED DATA
    # ========================================================

    if row_count < len(df):

        raise RuntimeError(
            "Database verification failed. "
            f"Expected at least {len(df)} rows, "
            f"but database contains {row_count}."
        )

    print(
        "Database verification passed!"
    )

    log_info(
        f"Database verification passed - "
        f"rows={row_count}"
    )


    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    cursor.close()
    cursor = None

    conn.close()
    conn = None

    print(
        "\nDatabase connection closed."
    )

    log_info(
        "Database connection closed successfully"
    )


# ============================================================
# ERROR HANDLING
# ============================================================

except Exception as error:

    print(
        "\nERROR: Database loading failed!"
    )

    print(
        "Reason:",
        error
    )

    log_exception(
        "Database loading failed"
    )


    # ========================================================
    # ROLLBACK
    # ========================================================

    if conn is not None:

        try:

            conn.rollback()

            print(
                "Transaction rolled back."
            )

            log_info(
                "Transaction rolled back successfully"
            )

        except Exception as rollback_error:

            print(
                "Rollback failed:",
                rollback_error
            )

            log_exception(
                "Database transaction rollback failed"
            )


    # ========================================================
    # CLOSE CURSOR
    # ========================================================

    if cursor is not None:

        try:

            cursor.close()

        except Exception as cleanup_error:

            log_warning(
                "Failed to close database cursor: "
                f"{cleanup_error}"
            )


    # ========================================================
    # CLOSE CONNECTION
    # ========================================================

    if conn is not None:

        try:

            conn.close()

        except Exception as cleanup_error:

            log_warning(
                "Failed to close database connection: "
                f"{cleanup_error}"
            )


    sys.exit(1)
