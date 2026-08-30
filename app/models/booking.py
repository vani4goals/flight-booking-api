from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class BookingStatus(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    pending = "pending"


class Booking(BaseModel):
    id: str
    flight_id: str
    passenger_name: str
    passenger_email: str
    seats: int
    status: BookingStatus
    booked_at: datetime
    total_price: float


class BookingCreate(BaseModel):
    flight_id: str
    passenger_name: str
    passenger_email: str
    seats: int


class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
