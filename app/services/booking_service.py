"""Business logic for creating and cancelling flight bookings.

Bookings are held in a process-local dictionary alongside the flight store in
`flight_service`. Creating and cancelling a booking writes through to that
store to keep seat counts in step, so the two modules share mutable state.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from app.models.booking import Booking, BookingCreate, BookingUpdate, BookingStatus
from app.services.flight_service import FlightService, _flights

# In-memory store — replace with a database in production
_bookings: dict[str, Booking] = {}

_flight_service = FlightService()


class BookingService:
    """Booking operations, including the seat accounting they imply."""

    def list_bookings(self) -> List[Booking]:
        """Return every stored booking, including cancelled-status ones."""
        return list(_bookings.values())

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Return the booking with this ID, or None if there is no such booking."""
        return _bookings.get(booking_id)

    def create_booking(self, payload: BookingCreate) -> Booking:
        """Book seats on a flight and return the confirmed booking.

        Deducts the booked seats from the flight's availability and prices the
        booking at the flight's current price times the seat count. The new
        booking's ID is generated here as a UUID4 string.

        Raises:
            ValueError: if the flight ID does not resolve, or if the flight has
                fewer seats available than requested.
        """
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
        """Apply a partial update to a booking and return the updated copy.

        Only the fields set on the payload are written; fields left as None are
        ignored. Returns None if no booking has this ID.

        Note that this does not touch seat availability. Setting the status to
        `cancelled` through this method marks the booking without returning its
        seats to the flight; `cancel_booking` is what restores them.
        """
        booking = _bookings.get(booking_id)
        if not booking:
            return None
        updated = booking.model_copy(update=payload.model_dump(exclude_none=True))
        _bookings[booking_id] = updated
        return updated

    def cancel_booking(self, booking_id: str) -> bool:
        """Delete a booking and return its seats to the flight.

        Returns True if the booking existed and False otherwise. The booking
        record is removed outright rather than kept with a cancelled status. If
        the referenced flight has since been deleted, the booking is still
        removed and the seat restoration is skipped.
        """
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
