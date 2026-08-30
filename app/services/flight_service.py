import uuid
from datetime import datetime
from typing import List, Optional
from app.models.flight import Flight, FlightCreate, FlightUpdate

# In-memory store — replace with a database in production
_flights: dict[str, Flight] = {}


class FlightService:
    def search_flights(self, origin: Optional[str], destination: Optional[str]) -> List[Flight]:
        results = list(_flights.values())
        if origin:
            results = [f for f in results if f.origin.lower() == origin.lower()]
        if destination:
            results = [f for f in results if f.destination.lower() == destination.lower()]
        return results

    def get_flight(self, flight_id: str) -> Optional[Flight]:
        return _flights.get(flight_id)

    def create_flight(self, payload: FlightCreate) -> Flight:
        flight = Flight(id=str(uuid.uuid4()), **payload.model_dump())
        _flights[flight.id] = flight
        return flight

    def update_flight(self, flight_id: str, payload: FlightUpdate) -> Optional[Flight]:
        flight = _flights.get(flight_id)
        if not flight:
            return None
        updated = flight.model_copy(update=payload.model_dump(exclude_none=True))
        _flights[flight_id] = updated
        return updated

    def delete_flight(self, flight_id: str) -> bool:
        if flight_id not in _flights:
            return False
        del _flights[flight_id]
        return True
