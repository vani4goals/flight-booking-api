import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.flight_service import _flights

client = TestClient(app)

SAMPLE_FLIGHT = {
    "origin": "NYC",
    "destination": "LAX",
    "departure_time": "2026-09-01T08:00:00",
    "arrival_time": "2026-09-01T11:30:00",
    "price": 299.99,
    "seats_available": 50,
    "airline": "SkyWay Airlines",
}


@pytest.fixture(autouse=True)
def clear_flights():
    _flights.clear()
    yield
    _flights.clear()


def test_create_flight():
    response = client.post("/flights/", json=SAMPLE_FLIGHT)
    assert response.status_code == 201
    data = response.json()
    assert data["origin"] == "NYC"
    assert data["destination"] == "LAX"
    assert "id" in data


def test_list_flights():
    client.post("/flights/", json=SAMPLE_FLIGHT)
    response = client.get("/flights/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_flights_by_origin():
    client.post("/flights/", json=SAMPLE_FLIGHT)
    response = client.get("/flights/?origin=NYC")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/flights/?origin=SFO")
    assert len(response.json()) == 0


def test_get_flight():
    created = client.post("/flights/", json=SAMPLE_FLIGHT).json()
    response = client.get(f"/flights/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_flight_not_found():
    response = client.get("/flights/nonexistent-id")
    assert response.status_code == 404


def test_update_flight():
    created = client.post("/flights/", json=SAMPLE_FLIGHT).json()
    response = client.patch(f"/flights/{created['id']}", json={"price": 199.99})
    assert response.status_code == 200
    assert response.json()["price"] == 199.99


def test_delete_flight():
    created = client.post("/flights/", json=SAMPLE_FLIGHT).json()
    response = client.delete(f"/flights/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/flights/{created['id']}")
    assert response.status_code == 404
