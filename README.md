# Flight Booking API

A sample REST API for searching and booking flights, built with **FastAPI** and **Pydantic v2**.

## Project Structure

```
flight-booking-api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app, root endpoint & router registration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── flight.py               # Flight, FlightCreate, FlightUpdate
│   │   └── booking.py              # Booking, BookingCreate, BookingUpdate, BookingStatus
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── flights.py              # Flight CRUD endpoints
│   │   └── bookings.py             # Booking endpoints
│   └── services/
│       ├── __init__.py
│       ├── flight_service.py       # Flight business logic & in-memory store
│       └── booking_service.py      # Booking business logic & seat accounting
├── tests/
│   ├── __init__.py
│   ├── test_flights.py
│   └── test_bookings.py
├── requirements.txt
└── README.md
```

The two service modules share mutable state: `booking_service` imports the
flight store from `flight_service` so that booking and cancellation can adjust
seat availability directly.

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app.main:app --reload
```

API docs available at: http://localhost:8000/docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |

### Flights
| Method | Path | Description |
|--------|------|-------------|
| GET | `/flights/` | List / search flights (`?origin=NYC&destination=LAX`) |
| GET | `/flights/{id}` | Get a flight by ID |
| POST | `/flights/` | Create a new flight |
| PATCH | `/flights/{id}` | Update price or seat count |
| DELETE | `/flights/{id}` | Remove a flight |

### Bookings
| Method | Path | Description |
|--------|------|-------------|
| GET | `/bookings/` | List all bookings |
| GET | `/bookings/{id}` | Get a booking by ID |
| POST | `/bookings/` | Book a flight |
| PATCH | `/bookings/{id}` | Update booking status |
| DELETE | `/bookings/{id}` | Cancel a booking (restores seats) |

## Running Tests

```bash
pytest tests/ -v
```

## Notes

- The in-memory store in `services/` is intentional for this template. Replace with SQLAlchemy + a real DB for production. All state is lost when the process exits.
- Seat availability is enforced at booking time and restored on cancellation. `DELETE /bookings/{id}` removes the booking record outright and returns its seats to the flight; setting the status to `cancelled` via `PATCH` marks the booking without restoring seats.
- Deleting a flight leaves any existing bookings pointing at an ID that no longer resolves.
