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