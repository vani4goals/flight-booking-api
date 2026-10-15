import uuid
from datetime import datetime, timezone

import pytest

from app.models.booking import BookingCreate, BookingStatus, BookingUpdate
from app.models.flight import FlightCreate
from app.services.booking_service import BookingService, _bookings
from app.services.flight_service import FlightService, _flights

SAMPLE_FLIGHT = FlightCreate(
    origin="NYC",
    destination="LAX",
    departure_time="2026-09-01T08:00:00",
    arrival_time="2026-09-01T11:30:00",
    price=299.99,
    seats_available=10,
    airline="SkyWay Airlines",
)


@pytest.fixture(autouse=True)
def clear_stores():
    _flights.clear()
    _bookings.clear()
    yield
    _flights.clear()
    _bookings.clear()


@pytest.fixture
def service():
    return BookingService()


@pytest.fixture
def flight():
    return FlightService().create_flight(SAMPLE_FLIGHT)


def make_payload(flight_id, seats=2):
    return BookingCreate(
        flight_id=flight_id,
        passenger_name="Alice Smith",
        passenger_email="alice@example.com",
        seats=seats,
    )


class TestListBookings:
    def test_empty_when_no_bookings(self, service):
        assert service.list_bookings() == []

    def test_returns_all_bookings(self, service, flight):
        first = service.create_booking(make_payload(flight.id, seats=1))
        second = service.create_booking(make_payload(flight.id, seats=1))
        ids = {b.id for b in service.list_bookings()}
        assert ids == {first.id, second.id}

    def test_includes_cancelled_status_bookings(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        service.update_booking(booking.id, BookingUpdate(status=BookingStatus.cancelled))
        [listed] = service.list_bookings()
        assert listed.status == BookingStatus.cancelled


class TestGetBooking:
    def test_returns_existing_booking(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        assert service.get_booking(booking.id) == booking

    def test_returns_none_for_unknown_id(self, service):
        assert service.get_booking("missing") is None


class TestCreateBooking:
    def test_returns_confirmed_booking_with_payload_fields(self, service, flight):
        booking = service.create_booking(make_payload(flight.id, seats=3))
        assert booking.flight_id == flight.id
        assert booking.passenger_name == "Alice Smith"
        assert booking.passenger_email == "alice@example.com"
        assert booking.seats == 3
        assert booking.status == BookingStatus.confirmed

    def test_generates_uuid4_id(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        assert uuid.UUID(booking.id).version == 4

    def test_ids_are_unique(self, service, flight):
        first = service.create_booking(make_payload(flight.id, seats=1))
        second = service.create_booking(make_payload(flight.id, seats=1))
        assert first.id != second.id

    def test_booked_at_is_current_utc_time(self, service, flight):
        before = datetime.now(timezone.utc)
        booking = service.create_booking(make_payload(flight.id))
        after = datetime.now(timezone.utc)
        assert booking.booked_at.tzinfo is not None
        assert before <= booking.booked_at <= after

    def test_total_price_is_flight_price_times_seats(self, service, flight):
        booking = service.create_booking(make_payload(flight.id, seats=3))
        assert booking.total_price == pytest.approx(299.99 * 3)

    def test_deducts_seats_from_flight(self, service, flight):
        service.create_booking(make_payload(flight.id, seats=4))
        assert _flights[flight.id].seats_available == 6

    def test_stores_booking(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        assert _bookings[booking.id] == booking

    def test_can_book_all_remaining_seats(self, service, flight):
        service.create_booking(make_payload(flight.id, seats=10))
        assert _flights[flight.id].seats_available == 0

    def test_unknown_flight_raises(self, service):
        with pytest.raises(ValueError, match="Flight missing not found"):
            service.create_booking(make_payload("missing"))
        assert _bookings == {}

    def test_insufficient_seats_raises_and_leaves_state_unchanged(self, service, flight):
        with pytest.raises(ValueError, match=r"Only 10 seat\(s\) available"):
            service.create_booking(make_payload(flight.id, seats=11))
        assert _flights[flight.id].seats_available == 10
        assert _bookings == {}


class TestUpdateBooking:
    def test_updates_status(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        updated = service.update_booking(booking.id, BookingUpdate(status=BookingStatus.pending))
        assert updated.status == BookingStatus.pending
        assert _bookings[booking.id].status == BookingStatus.pending

    def test_leaves_other_fields_unchanged(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        updated = service.update_booking(booking.id, BookingUpdate(status=BookingStatus.pending))
        assert updated.model_dump(exclude={"status"}) == booking.model_dump(exclude={"status"})

    def test_empty_payload_is_a_no_op(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        assert service.update_booking(booking.id, BookingUpdate()) == booking

    def test_cancelled_status_does_not_restore_seats(self, service, flight):
        booking = service.create_booking(make_payload(flight.id, seats=2))
        service.update_booking(booking.id, BookingUpdate(status=BookingStatus.cancelled))
        assert _flights[flight.id].seats_available == 8

    def test_returns_none_for_unknown_id(self, service):
        assert service.update_booking("missing", BookingUpdate(status=BookingStatus.pending)) is None
        assert _bookings == {}


class TestCancelBooking:
    def test_returns_true_and_removes_booking(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        assert service.cancel_booking(booking.id) is True
        assert service.get_booking(booking.id) is None

    def test_restores_seats_to_flight(self, service, flight):
        booking = service.create_booking(make_payload(flight.id, seats=3))
        service.cancel_booking(booking.id)
        assert _flights[flight.id].seats_available == 10

    def test_returns_false_for_unknown_id(self, service):
        assert service.cancel_booking("missing") is False

    def test_second_cancel_returns_false(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        service.cancel_booking(booking.id)
        assert service.cancel_booking(booking.id) is False
        assert _flights[flight.id].seats_available == 10

    def test_removes_booking_when_flight_was_deleted(self, service, flight):
        booking = service.create_booking(make_payload(flight.id))
        del _flights[flight.id]
        assert service.cancel_booking(booking.id) is True
        assert booking.id not in _bookings
        assert flight.id not in _flights
