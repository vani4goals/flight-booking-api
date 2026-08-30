from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Flight(BaseModel):
    id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    seats_available: int
    airline: str


class FlightCreate(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    seats_available: int
    airline: str


class FlightUpdate(BaseModel):
    price: Optional[float] = None
    seats_available: Optional[int] = None
