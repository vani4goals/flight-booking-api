from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.flight import Flight, FlightCreate, FlightUpdate
from app.services.flight_service import FlightService

router = APIRouter()
service = FlightService()


@router.get("/", response_model=List[Flight])
def list_flights(origin: Optional[str] = None, destination: Optional[str] = None):
    return service.search_flights(origin=origin, destination=destination)


@router.get("/{flight_id}", response_model=Flight)
def get_flight(flight_id: str):
    flight = service.get_flight(flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@router.post("/", response_model=Flight, status_code=201)
def create_flight(payload: FlightCreate):
    return service.create_flight(payload)


@router.patch("/{flight_id}", response_model=Flight)
def update_flight(flight_id: str, payload: FlightUpdate):
    flight = service.update_flight(flight_id, payload)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@router.delete("/{flight_id}", status_code=204)
def delete_flight(flight_id: str):
    if not service.delete_flight(flight_id):
        raise HTTPException(status_code=404, detail="Flight not found")
