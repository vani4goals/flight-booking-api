import uuid
from datetime import datetime

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

    def test_all_payload_fields_stored(self, service):
        flight = service.create_flight(SAMPLE_FLIGHT)
        assert flight.airline == "SkyWay Airlines"
        assert flight.seats_available == 50
        assert flight.departure_time == SAMPLE_FLIGHT.departure_time
        assert flight.arrival_time == SAMPLE_FLIGHT.arrival_time

    def test_id_is_a_uuid4_string(self, service):
        flight = service.create_flight(SAMPLE_FLIGHT)
        assert uuid.UUID(flight.id).version == 4

    def test_copies_every_payload_field(self, service):
        flight = service.create_flight(SAMPLE_FLIGHT)
        assert flight.departure_time == datetime(2026, 9, 1, 8, 0, 0)
        assert flight.arrival_time == datetime(2026, 9, 1, 11, 30, 0)
        assert flight.seats_available == 50
        assert flight.airline == "SkyWay Airlines"

    def test_does_not_mutate_payload(self, service):
        before = SAMPLE_FLIGHT.model_dump()
        service.create_flight(SAMPLE_FLIGHT)
        assert SAMPLE_FLIGHT.model_dump() == before

    def test_stores_each_flight_separately(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        assert len(_flights) == 2

    def test_rejects_payload_without_model_dump(self, service):
        with pytest.raises(AttributeError):
            service.create_flight({"origin": "NYC", "destination": "LAX"})

    def test_accepts_arrival_before_departure(self, service):
        # Documents current behaviour: the service performs no chronological
        # validation, so an impossible itinerary is stored as-is.
        backwards = SAMPLE_FLIGHT.model_copy(
            update={"arrival_time": datetime(2026, 8, 31, 8, 0, 0)}
        )
        flight = service.create_flight(backwards)
        assert flight.arrival_time < flight.departure_time


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

    def test_partial_origin_not_matched(self, service):
        # Docstring guarantees no partial/fuzzy matches — "NY" must not match "NYC"
        service.create_flight(SAMPLE_FLIGHT)
        assert service.search_flights("NY", None) == []

    def test_partial_destination_not_matched(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        assert service.search_flights(None, "LA") == []

    def test_both_filters_cross_miss_returns_empty(self, service):
        # NYC->LAX and SFO->ORD exist; NYC->ORD should yield nothing
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        assert service.search_flights("NYC", "ORD") == []

    def test_empty_string_origin_treated_as_no_filter(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        # "" is falsy — both flights should be returned
        results = service.search_flights("", None)
        assert len(results) == 2

    def test_empty_string_destination_treated_as_no_filter(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        results = service.search_flights(None, "")
        assert len(results) == 2

    def test_empty_string_filters_are_ignored(self, service):
        # Empty strings are falsy, so they behave like "no filter" rather than
        # matching flights with an empty origin/destination.
        service.create_flight(SAMPLE_FLIGHT)
        service.create_flight(OTHER_FLIGHT)
        assert len(service.search_flights("", "")) == 2

    def test_matches_stored_value_case_insensitively(self, service):
        service.create_flight(SAMPLE_FLIGHT.model_copy(update={"origin": "nyc"}))
        results = service.search_flights("NYC", None)
        assert len(results) == 1

    def test_does_not_match_origin_against_destination(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        assert service.search_flights("LAX", None) == []
        assert service.search_flights(None, "NYC") == []

    def test_untrimmed_filter_does_not_match(self, service):
        # The service compares case-insensitively but does not strip whitespace.
        service.create_flight(SAMPLE_FLIGHT)
        assert service.search_flights(" NYC ", None) == []

    def test_returns_stored_flight_objects(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        assert service.search_flights(None, None)[0] is _flights[created.id]

    def test_result_list_is_detached_from_store(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        results = service.search_flights(None, None)
        results.clear()
        assert len(service.search_flights(None, None)) == 1


class TestGetFlight:
    def test_returns_existing_flight(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        found = service.get_flight(created.id)
        assert found == created

    def test_returns_none_when_missing(self, service):
        assert service.get_flight("nonexistent-id") is None

    def test_returns_none_for_empty_id(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        assert service.get_flight("") is None

    def test_returns_the_stored_object(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        assert service.get_flight(created.id) is _flights[created.id]

    def test_returns_none_after_delete(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        service.delete_flight(created.id)
        assert service.get_flight(created.id) is None

    def test_lookup_requires_an_exact_id(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        assert service.get_flight(f" {created.id} ") is None


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

    def test_update_preserves_flight_id(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate(price=1.0))
        assert updated.id == created.id

    def test_update_seats_available_only(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate(seats_available=5))
        assert updated.seats_available == 5
        assert updated.price == created.price

    def test_explicit_none_is_ignored(self, service):
        # exclude_none means a field cannot be cleared through FlightUpdate.
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate(price=None))
        assert updated.price == created.price

    def test_applies_falsy_values(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(
            created.id, FlightUpdate(price=0.0, seats_available=0)
        )
        assert updated.price == 0.0
        assert updated.seats_available == 0

    def test_preserves_id_and_non_updatable_fields(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate(price=42.0))
        assert updated.id == created.id
        assert updated.origin == created.origin
        assert updated.destination == created.destination
        assert updated.departure_time == created.departure_time
        assert updated.arrival_time == created.arrival_time
        assert updated.airline == created.airline

    def test_stores_a_new_object_leaving_earlier_reference_stale(self, service):
        # model_copy returns a new instance, so a reference held from before the
        # update keeps the old values.
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(created.id, FlightUpdate(price=1.0))
        assert updated is not created
        assert created.price == 299.99
        assert _flights[created.id] is updated

    def test_does_not_affect_other_flights(self, service):
        first = service.create_flight(SAMPLE_FLIGHT)
        second = service.create_flight(OTHER_FLIGHT)
        service.update_flight(first.id, FlightUpdate(price=1.0))
        assert _flights[second.id] == second

    def test_returns_none_after_delete(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        service.delete_flight(created.id)
        assert service.update_flight(created.id, FlightUpdate(price=1.0)) is None

    def test_accepts_negative_values_without_validation(self, service):
        # Documents current behaviour: neither the model nor the service
        # constrains price or seat counts to non-negative numbers.
        created = service.create_flight(SAMPLE_FLIGHT)
        updated = service.update_flight(
            created.id, FlightUpdate(price=-10.0, seats_available=-5)
        )
        assert updated.price == -10.0
        assert updated.seats_available == -5


class TestDeleteFlight:
    def test_deletes_existing_flight(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        assert service.delete_flight(created.id) is True
        assert created.id not in _flights

    def test_returns_false_when_missing(self, service):
        assert service.delete_flight("nonexistent-id") is False

    def test_delete_twice_returns_false(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        service.delete_flight(created.id)
        assert service.delete_flight(created.id) is False

    def test_delete_leaves_other_flights_intact(self, service):
        first = service.create_flight(SAMPLE_FLIGHT)
        second = service.create_flight(OTHER_FLIGHT)
        service.delete_flight(first.id)
        assert second.id in _flights
        assert first.id not in _flights

    def test_delete_then_get_returns_none(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        service.delete_flight(created.id)
        assert service.get_flight(created.id) is None

    def test_second_delete_returns_false(self, service):
        created = service.create_flight(SAMPLE_FLIGHT)
        assert service.delete_flight(created.id) is True
        assert service.delete_flight(created.id) is False

    def test_returns_false_for_empty_id(self, service):
        service.create_flight(SAMPLE_FLIGHT)
        assert service.delete_flight("") is False
        assert len(_flights) == 1

    def test_does_not_affect_other_flights(self, service):
        first = service.create_flight(SAMPLE_FLIGHT)
        second = service.create_flight(OTHER_FLIGHT)
        service.delete_flight(first.id)
        assert service.get_flight(second.id) == second
        assert service.search_flights(None, None) == [second]


class TestSharedStore:
    def test_instances_share_the_same_store(self):
        writer, reader = FlightService(), FlightService()
        created = writer.create_flight(SAMPLE_FLIGHT)
        assert reader.get_flight(created.id) == created

    def test_delete_by_one_instance_is_visible_to_another(self):
        writer, reader = FlightService(), FlightService()
        created = writer.create_flight(SAMPLE_FLIGHT)
        assert reader.delete_flight(created.id) is True
        assert writer.get_flight(created.id) is None

    def test_update_by_one_instance_is_visible_to_another(self):
        writer, reader = FlightService(), FlightService()
        created = writer.create_flight(SAMPLE_FLIGHT)
        reader.update_flight(created.id, FlightUpdate(seats_available=3))
        assert writer.get_flight(created.id).seats_available == 3
