import uuid
from datetime import datetime, timezone
from typing import List, Optional
from app.models.booking import Booking, BookingCreate, BookingUpdate, BookingStatus
from app.services.flight_service import FlightService, _flights

# In-memory store — replace with a database in production
_bookings: dict[str, Booking] = {}

_flight_service = FlightService()


class BookingService:
    def list_bookings(self) -> List[Booking]:
        return list(_bookings.values())

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        return _bookings.get(booking_id)

    def create_booking(self, payload: BookingCreate) -> Booking:
        flight = _flight_service.get_flight(payload.flight_id)
        if not flight:
            raise ValueError(f"Flight {payload.flight_id} not found")
        if flight.seats_available < payload.seats:
            raise ValueError(f"Only {flight.seats_available} seat(s) available")

        total_price = flight.price * payload.seats
        booking = Booking(
            id=str(uuid.uuid4()),
            flight_id=payload.flight_id,
            passenger_name=payload.passenger_name,
            passenger_email=payload.passenger_email,
            seats=payload.seats,
            status=BookingStatus.confirmed,
            booked_at=datetime.now(timezone.utc),
            total_price=total_price,
        )
        # Deduct seats
        _flights[flight.id] = flight.model_copy(
            update={"seats_available": flight.seats_available - payload.seats}
        )
        _bookings[booking.id] = booking
        return booking

    def update_booking(self, booking_id: str, payload: BookingUpdate) -> Optional[Booking]:
        booking = _bookings.get(booking_id)
        if not booking:
            return None
        updated = booking.model_copy(update=payload.model_dump(exclude_none=True))
        _bookings[booking_id] = updated
        return updated

    def cancel_booking(self, booking_id: str) -> bool:
        booking = _bookings.get(booking_id)
        if not booking:
            return False
        # Restore seats on cancellation
        flight = _flight_service.get_flight(booking.flight_id)
        if flight:
            _flights[flight.id] = flight.model_copy(
                update={"seats_available": flight.seats_available + booking.seats}
            )
        del _bookings[booking_id]
        return True
