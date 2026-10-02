# Flight Booking API

A sample REST API for searching and booking flights, built with **FastAPI** and **Pydantic v2**.

## Prerequisites

- **Python 3.9 or newer** (developed and tested on Python 3.12). Check with `python3 --version`.
- `pip` (bundled with Python) and the built-in `venv` module.
- Optional: `curl` for trying the example requests below.

No database, message broker, or other external service is required — all data is kept in memory.

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
│   ├── test_flights.py             # API tests for /flights
│   ├── test_bookings.py            # API tests for /bookings
│   └── test_flight_service.py      # Unit tests for FlightService
├── requirements.txt
└── README.md
```

The two service modules share mutable state: `booking_service` imports the
flight store from `flight_service` so that booking and cancellation can adjust
seat availability directly.

## Quick Start

Run all commands from the project root (the directory containing `requirements.txt`).

### 1. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Windows (Command Prompt): `venv\Scripts\activate.bat`

Your prompt should now start with `(venv)`. Run the activate command again in every new terminal you open.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs everything needed to run the app **and** the tests: `fastapi`, `uvicorn[standard]`, `pydantic`, `pytest`, and `httpx` (used by FastAPI's `TestClient`).

### 3. Configuration

No configuration is needed. The app reads no environment variables or `.env` file, and there is no database to set up. The only options are the `uvicorn` command-line flags shown below (host, port, reload).

## Running the API locally

```bash
uvicorn app.main:app --reload
```

- `app.main:app` means "the `app` object in `app/main.py`", so run this from the project root.
- `--reload` restarts the server automatically when you edit code (for development only).
- The server listens on `http://127.0.0.1:8000` by default. To use a different port, add `--port 8080`. To accept connections from other machines, add `--host 0.0.0.0`.

Once it's running:

| URL | What it is |
|-----|------------|
| http://localhost:8000/ | Health/welcome message |
| http://localhost:8000/docs | Interactive Swagger UI (try endpoints in the browser) |
| http://localhost:8000/redoc | ReDoc API reference |

Press `Ctrl+C` to stop the server.

> **Note:** Data lives in memory only. The API starts **empty** (there is no seed data), and everything is lost when the server restarts — including every automatic restart triggered by `--reload`.

### Try it out

Create a flight (the response includes the generated `id`):

```bash
curl -X POST http://localhost:8000/flights/ \
  -H "Content-Type: application/json" \
  -d '{
        "origin": "NYC",
        "destination": "LAX",
        "departure_time": "2026-09-01T08:00:00",
        "arrival_time": "2026-09-01T11:30:00",
        "price": 299.99,
        "seats_available": 10,
        "airline": "SkyWay Airlines"
      }'
```

Search flights:

```bash
curl "http://localhost:8000/flights/?origin=NYC&destination=LAX"
```

Book seats on that flight (replace `<FLIGHT_ID>` with the `id` from the first response):

```bash
curl -X POST http://localhost:8000/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
        "flight_id": "<FLIGHT_ID>",
        "passenger_name": "Alice Smith",
        "passenger_email": "alice@example.com",
        "seats": 2
      }'
```

## Endpoints

All paths include a trailing slash, as shown.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |

### Flights
| Method | Path | Description |
|--------|------|-------------|
| GET | `/flights/` | List / search flights (`?origin=NYC&destination=LAX`, case-insensitive) |
| GET | `/flights/{id}` | Get a flight by ID |
| POST | `/flights/` | Create a new flight |
| PATCH | `/flights/{id}` | Update `price` and/or `seats_available` |
| DELETE | `/flights/{id}` | Remove a flight |

### Bookings
| Method | Path | Description |
|--------|------|-------------|
| GET | `/bookings/` | List all bookings |
| GET | `/bookings/{id}` | Get a booking by ID |
| POST | `/bookings/` | Book a flight (returns 400 if the flight doesn't exist or has too few seats) |
| PATCH | `/bookings/{id}` | Update booking `status` (`confirmed`, `pending`, `cancelled`) |
| DELETE | `/bookings/{id}` | Cancel a booking (restores seats) |

## Running Tests

With the virtual environment activated, from the project root:

```bash
pytest tests/ -v
```

The tests use FastAPI's `TestClient`, so you do **not** need the server running. Each test clears the in-memory stores, so tests are independent of each other and of any running server.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'app'`** — you are not in the project root. `cd` into the directory containing `app/` and `requirements.txt`, then rerun the command.
- **`uvicorn: command not found`** / **`pytest: command not found`** — the virtual environment isn't active (or dependencies weren't installed into it). Activate it and rerun `pip install -r requirements.txt`. Alternatively, use `python -m uvicorn ...` / `python -m pytest ...`.
- **`[Errno 48/98] Address already in use`** — another process is using port 8000. Stop it, or start on another port with `--port 8001`.
- **My flights/bookings disappeared** — expected. Storage is in memory and resets whenever the server restarts.

## Notes

- The in-memory store in `app/services/` is intentional for this template. Replace with SQLAlchemy + a real DB for production. All state is lost when the process exits.
- Seat availability is enforced at booking time and restored on cancellation. `DELETE /bookings/{id}` removes the booking record outright and returns its seats to the flight; setting the status to `cancelled` via `PATCH` marks the booking without restoring seats.
- Deleting a flight leaves any existing bookings pointing at an ID that no longer resolves.
