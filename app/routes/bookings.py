from fastapi import APIRouter, HTTPException
from typing import List
from app.models.booking import Booking, BookingCreate, BookingUpdate
from app.services.booking_service import BookingService

router = APIRouter()
service = BookingService()


@router.get("/", response_model=List[Booking])
def list_bookings():
    return service.list_bookings()


@router.get("/{booking_id}", response_model=Booking)
def get_booking(booking_id: str):
    booking = service.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/", response_model=Booking, status_code=201)
def create_booking(payload: BookingCreate):
    try:
        return service.create_booking(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{booking_id}", response_model=Booking)
def update_booking(booking_id: str, payload: BookingUpdate):
    booking = service.update_booking(booking_id, payload)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.delete("/{booking_id}", status_code=204)
def cancel_booking(booking_id: str):
    if not service.cancel_booking(booking_id):
        raise HTTPException(status_code=404, detail="Booking not found")
