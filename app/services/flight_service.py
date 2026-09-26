"""Business logic for flight search and management.

Flights are held in a process-local dictionary, so all state is lost when the
process exits. Replace `_flights` with a database layer for production use.
"""

import uuid
from datetime import datetime
from typing import List, Optional
from app.models.flight import Flight, FlightCreate, FlightUpdate

# In-memory store — replace with a database in production
_flights: dict[str, Flight] = {}


class FlightService:
    """CRUD and search operations over the in-memory flight store."""

    def search_flights(self, origin: Optional[str], destination: Optional[str]) -> List[Flight]:
        """Return flights matching the given origin and destination.

        Both filters are optional and are applied independently; passing None
        for both returns every stored flight. Matching is case-insensitive and
        requires the full code to match exactly (no partial or fuzzy matches).
        """
        results = list(_flights.values())
        if origin:
            results = [f for f in results if f.origin.lower() == origin.lower()]
        if destination:
            results = [f for f in results if f.destination.lower() == destination.lower()]
        return results

    def get_flight(self, flight_id: str) -> Optional[Flight]:
        """Return the flight with this ID, or None if no such flight exists."""
        return _flights.get(flight_id)

    def create_flight(self, payload: FlightCreate) -> Flight:
        """Store a new flight and return it.

        The ID is generated here as a UUID4 string; callers do not supply one.
        """
        flight = Flight(id=str(uuid.uuid4()), **payload.model_dump())
        _flights[flight.id] = flight
        return flight

    def update_flight(self, flight_id: str, payload: FlightUpdate) -> Optional[Flight]:
        """Apply a partial update to a flight and return the updated copy.

        Only the fields set on the payload are written; fields left as None are
        ignored rather than clearing the stored value. Returns None if no
        flight has this ID.
        """
        flight = _flights.get(flight_id)
        if not flight:
            return None
        updated = flight.model_copy(update=payload.model_dump(exclude_none=True))
        _flights[flight_id] = updated
        return updated

    def delete_flight(self, flight_id: str) -> bool:
        """Remove a flight, returning True if it existed and False otherwise.

        Existing bookings that reference this flight are left in place and will
        point at a flight ID that no longer resolves.
        """
        if flight_id not in _flights:
            return False
        del _flights[flight_id]
        return True
