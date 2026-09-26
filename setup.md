# Container Setup & Security Notes

## Docker Build Command

```bash
docker build -t flight-booking-api .
```

## Docker Run Command

```bash
docker run -it --rm \
  --name flight-booking-api \
  -v "$(pwd)":/workspace \
  -p 8000:8000 \
  --network host \
  -e ANTHROPIC_API_KEY=your_key_here \
  flight-booking-api
```

## Mounted Path

The project directory is mounted at `/workspace` inside the container:

```
-v "$(pwd)":/workspace
```

This means the agent sees live source files — edits made inside the container reflect immediately on the host, and vice versa.

## Network Mode

`--network host` — the container shares the host's network stack. This allows the FastAPI server running inside the container to be reachable at `http://localhost:8000` on the host without any extra port-mapping configuration.

## Smoke-Test Command

Run from the host against the already-running container:

```bash
docker exec flight-booking-api pytest tests/ -v
```

## Smoke-Test Output

```
============================= test session starts ==============================
platform linux -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
rootdir: /workspace
plugins: anyio-4.15.1
collecting ... collected 13 items

tests/test_bookings.py::test_create_booking PASSED                       [  7%]
tests/test_bookings.py::test_booking_reduces_available_seats PASSED      [ 15%]
tests/test_bookings.py::test_booking_insufficient_seats PASSED           [ 23%]
tests/test_bookings.py::test_booking_invalid_flight PASSED               [ 30%]
tests/test_bookings.py::test_cancel_booking_restores_seats PASSED        [ 38%]
tests/test_bookings.py::test_list_bookings PASSED                        [ 46%]
tests/test_flights.py::test_create_flight PASSED                         [ 53%]
tests/test_flights.py::test_list_flights PASSED                          [ 61%]
tests/test_flights.py::test_search_flights_by_origin PASSED              [ 69%]
tests/test_flights.py::test_get_flight PASSED                            [ 76%]
tests/test_flights.py::test_get_flight_not_found PASSED                  [ 84%]
tests/test_flights.py::test_update_flight PASSED                         [ 92%]
tests/test_flights.py::test_delete_flight PASSED                         [100%]

=============================== warnings summary ===============================
../usr/local/lib/python3.12/site-packages/fastapi/testclient.py:1
  /usr/local/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

../usr/local/lib/python3.12/site-packages/starlette/testclient.py:53
  /usr/local/lib/python3.12/site-packages/starlette/testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 13 passed, 2 warnings in 0.26s ===================
```

---

## Claude Code Smoke Test

Verify Claude Code is installed inside the container:

```bash
docker exec flight-booking-api claude --version
```

Output:

```
2.1.266 (Claude Code)
```

To run an interactive Claude prompt against the project (requires `ANTHROPIC_API_KEY` set at `docker run` time):

```bash
docker exec -it flight-booking-api claude "list the files in this project and describe what each one does"
```

Expected Claude response summarises `app/`, `tests/`, `Dockerfile`, `requirements.txt`, and the route/service/model split — confirming the agent can read the mounted workspace and reason about the code.

---

## API Verification (Insomnia / curl)

The following requests confirm the live API is reachable on `localhost:8000`.

### GET / — root health check

```bash
curl -s http://localhost:8000/
```

```json
{
    "message": "Welcome to the Flight Booking API"
}
```

### GET /flights/ — list flights

```bash
curl -s http://localhost:8000/flights/
```

```json
[
    {
        "id": "3bcd69b4-33f8-43f2-84d0-0b8d384cde33",
        "origin": "NYC",
        "destination": "LAX",
        "departure_time": "2026-09-20T08:00:00Z",
        "arrival_time": "2026-09-20T11:00:00Z",
        "price": 249.99,
        "seats_available": 38,
        "airline": "Delta"
    }
]
```

### GET /docs — Swagger UI

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs
```

```
200
```

Interactive docs are available at `http://localhost:8000/docs` — equivalent to sending these requests through Insomnia.

---

## Security Decisions (Provisional)

### What network mode did you choose and why?
`--network host` was chosen for simplicity during the course — it lets the FastAPI server be accessible at `localhost:8000` without extra configuration. The trade-off is that the container shares the host's full network stack, which is broader access than necessary. In a shared or production environment this would be replaced with a narrowly scoped bridge network exposing only port 8000.

### What did you mount and why?
Only the project directory (`$(pwd)` → `/workspace`) is mounted. This gives the agent access to source files and tests without exposing the rest of the host filesystem. No home directory, credentials folder, or system paths are mounted.

### What credentials does the container need?
The `ANTHROPIC_API_KEY` is passed via `-e` at runtime rather than baked into the image. The app itself uses in-memory storage and requires no database credentials or other secrets.

### What tools are included in the image and why?
- **Claude Code** — the primary AI coding agent for this course
- **OpenCode** — secondary agent tool included by the course template
- **ngrok** — included to expose the local server for external testing if needed

At this stage all three are from the course-provided Dockerfile. As the project evolves, tools that have no active use should be removed to reduce the image's attack surface.

### What would you restrict in a production or shared environment?
- Switch from `--network host` to a named bridge network with only port 8000 exposed
- Run the container as a non-root user
- Remove ngrok and OpenCode if not actively used
- Use Docker secrets or a secrets manager instead of passing `ANTHROPIC_API_KEY` via `-e`
- Add a read-only filesystem flag (`--read-only`) with explicit write mounts only for `/workspace`

These choices are provisional and will be revisited as the project grows throughout the course.
