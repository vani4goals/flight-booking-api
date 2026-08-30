# Flight Booking API

A sample REST API for searching and booking flights, built with **FastAPI** and **Pydantic v2**.

## Project Structure

```
flight-booking-api/
├── app/
│   ├── main.py              # FastAPI app & router registration
│   ├── models/
│   │   ├── flight.py        # Flight Pydantic models
│   │   └── booking.py       # Booking Pydantic models
│   ├── routes/
│   │   ├── flights.py       # Flight CRUD endpoints
│   │   └── bookings.py      # Booking endpoints
│   └── services/
│       ├── flight_service.py   # Flight business logic
│       └── booking_service.py  # Booking business logic
├── tests/
│   ├── test_flights.py
│   └── test_bookings.py
├── requirements.txt
└── .gitignore
```

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

- The in-memory store in `services/` is intentional for this template. Replace with SQLAlchemy + a real DB for production.
- Seat availability is enforced at booking time and restored on cancellation.
