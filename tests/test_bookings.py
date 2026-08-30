import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.flight_service import _flights
from app.services.booking_service import _bookings

client = TestClient(app)

SAMPLE_FLIGHT = {
    "origin": "NYC",
    "destination": "LAX",
    "departure_time": "2026-09-01T08:00:00",
    "arrival_time": "2026-09-01T11:30:00",
    "price": 299.99,
    "seats_available": 10,
    "airline": "SkyWay Airlines",
}


@pytest.fixture(autouse=True)
def clear_stores():
    _flights.clear()
    _bookings.clear()
    yield
    _flights.clear()
    _bookings.clear()


@pytest.fixture
def flight_id():
    response = client.post("/flights/", json=SAMPLE_FLIGHT)
    return response.json()["id"]


def test_create_booking(flight_id):
    payload = {
        "flight_id": flight_id,
        "passenger_name": "Alice Smith",
        "passenger_email": "alice@example.com",
        "seats": 2,
    }
    response = client.post("/bookings/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["seats"] == 2
    assert data["total_price"] == pytest.approx(599.98)
    assert data["status"] == "confirmed"


def test_booking_reduces_available_seats(flight_id):
    client.post("/bookings/", json={
        "flight_id": flight_id,
        "passenger_name": "Bob",
        "passenger_email": "bob@example.com",
        "seats": 3,
    })
    flight = client.get(f"/flights/{flight_id}").json()
    assert flight["seats_available"] == 7


def test_booking_insufficient_seats(flight_id):
    response = client.post("/bookings/", json={
        "flight_id": flight_id,
        "passenger_name": "Bob",
        "passenger_email": "bob@example.com",
        "seats": 99,
    })
    assert response.status_code == 400


def test_booking_invalid_flight():
    response = client.post("/bookings/", json={
        "flight_id": "nonexistent",
        "passenger_name": "Bob",
        "passenger_email": "bob@example.com",
        "seats": 1,
    })
    assert response.status_code == 400


def test_cancel_booking_restores_seats(flight_id):
    booking = client.post("/bookings/", json={
        "flight_id": flight_id,
        "passenger_name": "Carol",
        "passenger_email": "carol@example.com",
        "seats": 4,
    }).json()

    client.delete(f"/bookings/{booking['id']}")
    flight = client.get(f"/flights/{flight_id}").json()
    assert flight["seats_available"] == 10


def test_list_bookings(flight_id):
    client.post("/bookings/", json={
        "flight_id": flight_id,
        "passenger_name": "Dan",
        "passenger_email": "dan@example.com",
        "seats": 1,
    })
    response = client.get("/bookings/")
    assert response.status_code == 200
    assert len(response.json()) == 1
