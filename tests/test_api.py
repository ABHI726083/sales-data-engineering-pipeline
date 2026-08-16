from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


# ============================================================
# ROOT ENDPOINT
# ============================================================

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Sales Data Engineering API is running"
    }


# ============================================================
# HEALTH ENDPOINT
# ============================================================

def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "database": "connected"
    }


# ============================================================
# SALES ENDPOINT
# ============================================================

def test_sales_endpoint():

    response = client.get("/sales")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) == 11


# ============================================================
# SALES RECORD STRUCTURE
# ============================================================

def test_sales_record_structure():

    response = client.get("/sales")

    data = response.json()

    expected_fields = {
        "order_id",
        "order_date",
        "product",
        "category",
        "quantity",
        "price",
        "city",
        "total_sales",
    }

    assert expected_fields.issubset(
        data[0].keys()
    )


# ============================================================
# SUMMARY ANALYTICS
# ============================================================

def test_summary_endpoint():

    response = client.get(
        "/analytics/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_orders"] == 11

    assert data["total_quantity"] == 41

    assert data["total_sales"] == 301500.0


# ============================================================
# CITY ANALYTICS
# ============================================================

def test_city_analytics_endpoint():

    response = client.get(
        "/analytics/city"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["city"] == "Delhi"

    assert data[0]["total_sales"] == 198500


# ============================================================
# CATEGORY ANALYTICS
# ============================================================

def test_category_analytics_endpoint():

    response = client.get(
        "/analytics/category"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["category"] == "Electronics"

    assert data[0]["total_sales"] == 250500

    assert data[1]["category"] == "Furniture"

    assert data[1]["total_sales"] == 51000


# ============================================================
# PRODUCT ANALYTICS
# ============================================================

def test_product_analytics_endpoint():

    response = client.get(
        "/analytics/product"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["product"] == "Laptop"

    assert data[0]["total_sales"] == 165000

    assert data[1]["product"] == "Monitor"

    assert data[1]["total_sales"] == 60000


# ============================================================
# CITY FILTER
# ============================================================

def test_sales_city_filter():

    response = client.get(
        "/sales?city=Delhi"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5

    for record in data:

        assert record["city"] == "Delhi"


# ============================================================
# CATEGORY FILTER
# ============================================================

def test_sales_category_filter():

    response = client.get(
        "/sales?category=Electronics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 7

    for record in data:

        assert record["category"] == "Electronics"


# ============================================================
# PRODUCT FILTER
# ============================================================

def test_sales_product_filter():

    response = client.get(
        "/sales?product=Laptop"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for record in data:

        assert record["product"] == "Laptop"


# ============================================================
# SALES LIMIT
# ============================================================

def test_sales_limit():

    response = client.get(
        "/sales?limit=3"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    assert data[0]["order_id"] == 1001

    assert data[2]["order_id"] == 1003


# ============================================================
# SALES OFFSET
# ============================================================

def test_sales_offset():

    response = client.get(
        "/sales?limit=3&offset=3"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

    assert data[0]["order_id"] == 1004

    assert data[2]["order_id"] == 1006


# ============================================================
# SALES FILTER WITH PAGINATION
# ============================================================

def test_sales_filter_with_pagination():

    response = client.get(
        "/sales?city=Delhi&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for record in data:

        assert record["city"] == "Delhi"


# ============================================================
# INVALID LIMIT - TOO SMALL
# ============================================================

def test_sales_invalid_limit_zero():

    response = client.get(
        "/sales?limit=0"
    )

    assert response.status_code == 422


# ============================================================
# INVALID LIMIT - TOO LARGE
# ============================================================

def test_sales_invalid_limit_too_large():

    response = client.get(
        "/sales?limit=1001"
    )

    assert response.status_code == 422


# ============================================================
# INVALID OFFSET - NEGATIVE
# ============================================================

def test_sales_invalid_offset():

    response = client.get(
        "/sales?offset=-1"
    )

    assert response.status_code == 422


# ============================================================
# UNKNOWN CITY
# ============================================================

def test_sales_unknown_city():

    response = client.get(
        "/sales?city=UnknownCity"
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []


# ============================================================
# UNKNOWN CATEGORY
# ============================================================

def test_sales_unknown_category():

    response = client.get(
        "/sales?category=UnknownCategory"
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []


# ============================================================
# UNKNOWN PRODUCT
# ============================================================

def test_sales_unknown_product():

    response = client.get(
        "/sales?product=UnknownProduct"
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []


# ============================================================
# COMBINED CITY + CATEGORY FILTER
# ============================================================

def test_sales_city_and_category_filter():

    response = client.get(
        "/sales?city=Delhi&category=Electronics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 4

    for record in data:

        assert record["city"] == "Delhi"

        assert record["category"] == "Electronics"


# ============================================================
# COMBINED CITY + PRODUCT FILTER
# ============================================================

def test_sales_city_and_product_filter():

    response = client.get(
        "/sales?city=Delhi&product=Laptop"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["city"] == "Delhi"

    assert data[0]["product"] == "Laptop"

    assert data[0]["order_id"] == 1001