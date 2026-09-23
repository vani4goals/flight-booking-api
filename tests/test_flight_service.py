import pytest

from app.models.flight import FlightCreate, FlightUpdate
from app.services.flight_service import FlightService, _flights

SAMPLE_FLIGHT = FlightCreate(
    origin="NYC",
    destination="LAX",
    departure_time="2026-09-01T08:00:00",
    arrival_time="2026-09-01T11:30:00",
    price=299.99,
    seats_available=50,
    airline="SkyWay Airlines",
)

OTHER_FLIGHT = FlightCreate(
    origin="SFO",
    destination="ORD",
    departure_time="2026-09-02T09:00:00",
    arrival_time="2026-09-02T14:00:00",
    price=199.50,
    seats_available=20,
    airline="Continental Air",
)


@pytest.fixture(autouse=True)
def clear_flights():
    _flights.clear()
    yield
    _flights.clear()


@pytest.fixture
def service():
    return FlightService()


class TestCreateFlight:
    def test_returns_flight_with_generated_id(self, service):
        flight = service.create_flight(SAMPLE_FLIGHT)
        assert flight.id
        assert flight.origin == "NYC"
        assert flight.destination == "LAX"
        assert flight.price == 299.99

    def test_persists_flight_in_store(self, service):
        flight = service.create_flight(SAMPLE_FLIGHT)
        assert _flights[flight.id] == flight

    def test_generates_unique_ids(self, service):
        first = service.create_flight(SAMPLE_FLIGHT)
        second = service.create_flight(SAMPLE_FLIGHT)
        assert first.id != second.id


class TestSearchFlights:
    def test_no_filters_returns_all(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        results = service.search_flights(None, None)
        assert len(results) == 2

    def test_filters_by_origin_case_insensitive(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        results = service.search_flights("nyc", None)
        assert len(results) == 1
        assert results[0].origin == "NYC"

    def test_filters_by_destination_case_insensitive(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        results = service.search_flights(None, "ord")
        assert len(results) == 1
        assert results[0].destination == "ORD"

    def test_filters_by_origin_and_destination(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        results = service.search_flights("NYC", "LAX")
        assert len(results) == 1

    def test_no_match_returns_empty_list(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        results = service.search_flights("SFO", None)
        assert results == []

    def test_empty_store_returns_empty_list(self, service):
        assert service.search_flights(None, None) == []


class TestGetFlight:
    def test_returns_existing_flight(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        found = service.get_flight(created.id)
        assert found == created

    def test_returns_none_when_missing(self, service):
        assert service.get_flight("nonexistent-id") is None


class TestUpdateFlight:
    def test_updates_provided_fields(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate(price=199.99))
        assert updated.price == 199.99
        assert updated.seats_available == created.seats_available

    def test_updates_multiple_fields(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(
            created.id, FlightUpdate(price=150.0, seats_available=10)
        )
        assert updated.price == 150.0
        assert updated.seats_available == 10

    def test_leaves_unset_fields_unchanged(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate())
        assert updated == created

    def test_persists_update_in_store(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        service.update_flight(created.id, FlightUpdate(price=1.0))
        assert _flights[created.id].price == 1.0

    def test_returns_none_when_missing(self, service):
        result = service.update_flight("nonexistent-id", FlightUpdate(price=1.0))
        assert result is None


class TestDeleteFlight:
    def test_deletes_existing_flight(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        assert service.delete_flight(created.id) is True
        assert created.id not in _flights

    def test_returns_false_when_missing(self, service):
        assert service.delete_flight("nonexistent-id") is False
