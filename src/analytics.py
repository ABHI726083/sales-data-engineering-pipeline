import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

# Sales by City
cursor.execute("""
    SELECT city, SUM(total_sales) AS total_sales
    FROM sales
    GROUP BY city
    ORDER BY total_sales DESC;
""")

results = cursor.fetchall()

print("Sales by City:")
for city, total_sales in results:
    print(city, ":", total_sales)


# Sales by Category
cursor.execute("""
    SELECT category, SUM(total_sales) AS total_sales
    FROM sales
    GROUP BY category
    ORDER BY total_sales DESC;
""")

results = cursor.fetchall()

print("\nSales by Category:")
for category, total_sales in results:
    print(category, ":", total_sales)


# Sales by Product
cursor.execute("""
    SELECT product, SUM(total_sales) AS total_sales
    FROM sales
    GROUP BY product
    ORDER BY total_sales DESC;
""")

results = cursor.fetchall()

print("\nSales by Product:")
for product, total_sales in results:
    print(product, ":", total_sales)


# Total Quantity Sold
cursor.execute("""
    SELECT SUM(quantity)
    FROM sales;
""")

total_quantity = cursor.fetchone()[0]

print("\nTotal Quantity Sold:", total_quantity)

cursor.close()
conn.close()