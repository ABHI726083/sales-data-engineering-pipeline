from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Sales Data Engineering API is running"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_sales_endpoint():
    response = client.get("/sales")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) == 11


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

    assert expected_fields.issubset(data[0].keys())
def test_summary_endpoint():
    response = client.get("/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_orders"] == 11
    assert data["total_quantity"] == 41
    assert data["total_sales"] == 301500.0
def test_city_analytics_endpoint():
    response = client.get("/analytics/city")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["city"] == "Delhi"
    assert data[0]["total_sales"] == 198500
def test_category_analytics_endpoint():
    response = client.get("/analytics/category")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["category"] == "Electronics"
    assert data[0]["total_sales"] == 250500

    assert data[1]["category"] == "Furniture"
    assert data[1]["total_sales"] == 51000
def test_product_analytics_endpoint():
    response = client.get("/analytics/product")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert data[0]["product"] == "Laptop"
    assert data[0]["total_sales"] == 165000

    assert data[1]["product"] == "Monitor"
    assert data[1]["total_sales"] == 60000 
def test_sales_city_filter():
    response = client.get("/sales?city=Delhi")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5

    for record in data:
        assert record["city"] == "Delhi"


def test_sales_category_filter():
    response = client.get("/sales?category=Electronics")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 7

    for record in data:
        assert record["category"] == "Electronics"


def test_sales_product_filter():
    response = client.get("/sales?product=Laptop")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for record in data:
        assert record["product"] == "Laptop"