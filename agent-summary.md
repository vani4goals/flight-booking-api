# Flight Booking API — Project Summary

## What the project does

A sample REST API for searching and booking flights. It lets clients create and query flights, make bookings (with seat-availability enforcement), update booking status, and cancel bookings (which restores seat counts). Built with **FastAPI** and **Pydantic v2**; data is held in-memory (no database).

## Main directories

| Path | Purpose |
|------|---------|
| `app/` | Application source |
| `app/models/` | Pydantic data models |
| `app/routes/` | FastAPI routers (HTTP endpoints) |
| `app/services/` | Business logic and in-memory data store |
| `tests/` | Pytest test suite |

## Important files

| File | Role |
|------|------|
| `app/main.py` | FastAPI app entry point; mounts `/flights` and `/bookings` routers |
| `app/models/flight.py` | `Flight`, `FlightCreate`, `FlightUpdate` schemas |
| `app/models/booking.py` | `Booking`, `BookingCreate`, `BookingUpdate` schemas; `BookingStatus` enum |
| `app/routes/flights.py` | CRUD endpoints for flights (list/search, get, create, patch, delete) |
| `app/routes/bookings.py` | Booking endpoints (list, get, create, patch, delete/cancel) |
| `app/services/flight_service.py` | In-memory flight store and search logic |
| `app/services/booking_service.py` | In-memory booking store; enforces seat availability |
| `tests/test_flights.py` | Tests for flight endpoints |
| `tests/test_bookings.py` | Tests for booking endpoints |
| `requirements.txt` | Python dependencies: fastapi, uvicorn, pydantic, pytest, httpx |
| `Dockerfile` | Container image (Python 3.12-slim); also installs Claude Code, OpenCode, and ngrok for the course environment |
| `docker-entrypoint.sh` | Container startup script |

## Key endpoints

**Flights** (`/flights`)
- `GET /flights/` — list/search flights (`?origin=`, `?destination=`)
- `GET /flights/{id}` — get by ID
- `POST /flights/` — create
- `PATCH /flights/{id}` — update price or seat count
- `DELETE /flights/{id}` — delete

**Bookings** (`/bookings`)
- `GET /bookings/` — list all bookings
- `GET /bookings/{id}` — get by ID
- `POST /bookings/` — book a flight (deducts seats)
- `PATCH /bookings/{id}` — update status
- `DELETE /bookings/{id}` — cancel (restores seats)

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# API docs: http://localhost:8000/docs

pytest tests/ -v
```
