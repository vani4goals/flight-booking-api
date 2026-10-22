# Flight Booking API — Test Execution Report

- **Date:** 2026-10-22
- **Working directory / rootdir:** `/workspace`
- **Scope:** Execute the existing test suite as-is. No application source, test, or configuration files were modified, and no dependencies were installed.

## Command

The suite was executed exactly as specified, from the repository root:

```bash
python -m pytest -v
```

Exit code: **0**

## Test Configuration

The repository contains **no pytest configuration file**. Verified absent at the repository root and in subdirectories (depth 3): `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini`, and any `conftest.py`. The run therefore used pytest defaults throughout — default test discovery (`test_*.py`), no custom markers, no coverage plugin, no warning filters, and no options injected via `addopts`.

`rootdir` was resolved to `/workspace` and `cachedir` to `.pytest_cache`. `tests/__init__.py` is present, so the test directory is an importable package and `app` resolves from the rootdir on `sys.path`.

Declared dependencies (`requirements.txt`):

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pytest>=8.2.0
httpx>=0.27.0
```

### Environment

| Component | Version |
|---|---|
| Platform | linux (Linux 7.0.12-linuxkit) |
| Python | 3.12.14 (`/usr/local/bin/python3`) |
| pytest | 9.1.1 |
| pluggy | 1.6.0 |
| Plugins | anyio-4.15.1 |
| fastapi | 0.141.1 |
| starlette | 1.6.0 |
| pydantic | 2.13.5 (pydantic_core 2.46.5) |
| httpx | 0.28.1 |
| uvicorn | 0.52.4 |

### Test Files Discovered

| File | Tests | Focus |
|---|---|---|
| `tests/test_bookings.py` | 6 | Booking API endpoints via `TestClient` |
| `tests/test_flight_service.py` | 29 | `FlightService` unit tests (5 test classes) |
| `tests/test_flights.py` | 7 | Flight API endpoints via `TestClient` |
| **Total** | **42** | |

## Results

| Outcome | Count |
|---|---|
| Passed | 42 |
| Failed | 0 |
| Skipped | 0 |
| Errors | 0 |
| xfailed / xpassed | 0 |
| Warnings | 2 |

**Execution duration: 0.19 s** (as reported in the pytest summary line: `42 passed, 2 warnings in 0.19s`).

Summary line:

```
======================== 42 passed, 2 warnings in 0.19s ========================
```

### Per-Test Results

All 42 tests reported `PASSED`.

#### `tests/test_bookings.py` — 6 passed

| Test | Result |
|---|---|
| `test_create_booking` | PASSED |
| `test_booking_reduces_available_seats` | PASSED |
| `test_booking_insufficient_seats` | PASSED |
| `test_booking_invalid_flight` | PASSED |
| `test_cancel_booking_restores_seats` | PASSED |
| `test_list_bookings` | PASSED |

#### `tests/test_flight_service.py` — 29 passed

| Class | Test | Result |
|---|---|---|
| `TestCreateFlight` | `test_returns_flight_with_generated_id` | PASSED |
| `TestCreateFlight` | `test_persists_flight_in_store` | PASSED |
| `TestCreateFlight` | `test_generates_unique_ids` | PASSED |
| `TestCreateFlight` | `test_all_payload_fields_stored` | PASSED |
| `TestSearchFlights` | `test_no_filters_returns_all` | PASSED |
| `TestSearchFlights` | `test_filters_by_origin_case_insensitive` | PASSED |
| `TestSearchFlights` | `test_filters_by_destination_case_insensitive` | PASSED |
| `TestSearchFlights` | `test_filters_by_origin_and_destination` | PASSED |
| `TestSearchFlights` | `test_no_match_returns_empty_list` | PASSED |
| `TestSearchFlights` | `test_empty_store_returns_empty_list` | PASSED |
| `TestSearchFlights` | `test_partial_origin_not_matched` | PASSED |
| `TestSearchFlights` | `test_partial_destination_not_matched` | PASSED |
| `TestSearchFlights` | `test_both_filters_cross_miss_returns_empty` | PASSED |
| `TestSearchFlights` | `test_empty_string_origin_treated_as_no_filter` | PASSED |
| `TestSearchFlights` | `test_empty_string_destination_treated_as_no_filter` | PASSED |
| `TestGetFlight` | `test_returns_existing_flight` | PASSED |
| `TestGetFlight` | `test_returns_none_when_missing` | PASSED |
| `TestUpdateFlight` | `test_updates_provided_fields` | PASSED |
| `TestUpdateFlight` | `test_updates_multiple_fields` | PASSED |
| `TestUpdateFlight` | `test_leaves_unset_fields_unchanged` | PASSED |
| `TestUpdateFlight` | `test_persists_update_in_store` | PASSED |
| `TestUpdateFlight` | `test_returns_none_when_missing` | PASSED |
| `TestUpdateFlight` | `test_update_preserves_flight_id` | PASSED |
| `TestUpdateFlight` | `test_update_seats_available_only` | PASSED |
| `TestDeleteFlight` | `test_deletes_existing_flight` | PASSED |
| `TestDeleteFlight` | `test_returns_false_when_missing` | PASSED |
| `TestDeleteFlight` | `test_delete_twice_returns_false` | PASSED |
| `TestDeleteFlight` | `test_delete_leaves_other_flights_intact` | PASSED |
| `TestDeleteFlight` | `test_delete_then_get_returns_none` | PASSED |

#### `tests/test_flights.py` — 7 passed

| Test | Result |
|---|---|
| `test_create_flight` | PASSED |
| `test_list_flights` | PASSED |
| `test_search_flights_by_origin` | PASSED |
| `test_get_flight` | PASSED |
| `test_get_flight_not_found` | PASSED |
| `test_update_flight` | PASSED |
| `test_delete_flight` | PASSED |

## Warnings

Two warnings were raised, both at import/collection time from third-party packages. Neither originates in this repository's `app/` or `tests/` code, and neither is caused by a failing assertion.

**1. `StarletteDeprecationWarning` — `fastapi/testclient.py:1`**

```
/usr/local/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa
```

Starlette 1.6.0 now prefers `httpx2` as the transport behind `TestClient`; the installed `httpx` 0.28.1 still works but is on a deprecation path. Triggered by `tests/test_bookings.py` and `tests/test_flights.py`, which both import `fastapi.testclient.TestClient`.

**2. `DeprecationWarning` — `starlette/testclient.py:53`**

```
/usr/local/lib/python3.12/site-packages/starlette/testclient.py:53: DeprecationWarning:
The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
  _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]
```

An internal Starlette reference to an anyio alias deprecated in anyio 4.15.1. Resolved upstream, not in application code.

## Observations

- **Full green suite.** 42 of 42 tests passed with no failures, errors, or skips. Exit code 0 confirms the result.
- **No skipped tests and no skip machinery.** No `@pytest.mark.skip`/`skipif`/`xfail` markers exist anywhere in the suite, so the zero-skip count reflects the suite's design rather than conditional skipping that happened to be inactive in this environment.
- **Runtime is effectively instantaneous (0.19 s).** The suite is fully in-process: `TestClient` exercises the ASGI app directly with no network or server startup, and both services use in-memory dicts with no database or I/O. There is no fixture or collection hot spot worth tuning.
- **Dependency versions run well ahead of the declared floors.** `requirements.txt` only pins lower bounds, and the resolved environment is substantially newer (fastapi 0.141.1 vs `>=0.111.0`; pytest 9.1.1 vs `>=8.2.0`; starlette at a 1.x major). The suite is nonetheless fully compatible with these versions — both warnings are deprecation notices, not behavioral breaks. The absence of upper bounds does mean a future `httpx`/`starlette` major could turn warning 1 into a hard failure.
- **Test isolation is handled explicitly and appears sound.** Each test module defines an `autouse` fixture that clears the module-level `_flights` (and `_bookings`) stores both before and after every test. This matters because `app/services/booking_service.py` mutates the flight store imported from `flight_service`, making the shared state cross-module. The clean run with no ordering-dependent failures suggests the teardown is working as intended.
- **Coverage is skewed toward the flight service.** 29 of 42 tests (69%) target `FlightService` directly, including edge cases such as partial-match rejection and empty-string filters. By comparison the booking path has 6 endpoint tests and no dedicated unit-test module for `BookingService`, and the `PATCH /bookings/{id}` status-update endpoint and `GET /bookings/{id}` are not exercised by any test. Behavior the README calls out explicitly — that `PATCH` to `cancelled` marks a booking *without* restoring seats, unlike `DELETE` — is untested. This is an observation about the existing suite, not a defect found by this run.
- **No coverage measurement is configured.** `pytest-cov` is neither installed nor declared, so line/branch coverage figures are unavailable from this run; the coverage comments above are based on reading the tests, not on instrumentation.
- **Stale bytecode from another interpreter is present.** `app/` contains `__pycache__` entries for both `cpython-312` and `cpython-314`, indicating the repository was previously run under Python 3.14. The current run used 3.12.14 and was unaffected.
- **The README's project structure is out of date.** It lists only `test_flights.py` and `test_bookings.py` under `tests/`; `test_flight_service.py` — the largest module in the suite — is missing from that listing.

## Evidence

Verbatim console output of the run:

```
============================= test session starts ==============================
platform linux -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /workspace
plugins: anyio-4.15.1
collecting ... collected 42 items

tests/test_bookings.py::test_create_booking PASSED                       [  2%]
tests/test_bookings.py::test_booking_reduces_available_seats PASSED      [  4%]
tests/test_bookings.py::test_booking_insufficient_seats PASSED           [  7%]
tests/test_bookings.py::test_booking_invalid_flight PASSED               [  9%]
tests/test_bookings.py::test_cancel_booking_restores_seats PASSED        [ 11%]
tests/test_bookings.py::test_list_bookings PASSED                        [ 14%]
tests/test_flight_service.py::TestCreateFlight::test_returns_flight_with_generated_id PASSED [ 16%]
tests/test_flight_service.py::TestCreateFlight::test_persists_flight_in_store PASSED [ 19%]
tests/test_flight_service.py::TestCreateFlight::test_generates_unique_ids PASSED [ 21%]
tests/test_flight_service.py::TestCreateFlight::test_all_payload_fields_stored PASSED [ 23%]
tests/test_flight_service.py::TestSearchFlights::test_no_filters_returns_all PASSED [ 26%]
tests/test_flight_service.py::TestSearchFlights::test_filters_by_origin_case_insensitive PASSED [ 28%]
tests/test_flight_service.py::TestSearchFlights::test_filters_by_destination_case_insensitive PASSED [ 30%]
tests/test_flight_service.py::TestSearchFlights::test_filters_by_origin_and_destination PASSED [ 33%]
tests/test_flight_service.py::TestSearchFlights::test_no_match_returns_empty_list PASSED [ 35%]
tests/test_flight_service.py::TestSearchFlights::test_empty_store_returns_empty_list PASSED [ 38%]
tests/test_flight_service.py::TestSearchFlights::test_partial_origin_not_matched PASSED [ 40%]
tests/test_flight_service.py::TestSearchFlights::test_partial_destination_not_matched PASSED [ 42%]
tests/test_flight_service.py::TestSearchFlights::test_both_filters_cross_miss_returns_empty PASSED [ 45%]
tests/test_flight_service.py::TestSearchFlights::test_empty_string_origin_treated_as_no_filter PASSED [ 47%]
tests/test_flight_service.py::TestSearchFlights::test_empty_string_destination_treated_as_no_filter PASSED [ 50%]
tests/test_flight_service.py::TestGetFlight::test_returns_existing_flight PASSED [ 52%]
tests/test_flight_service.py::TestGetFlight::test_returns_none_when_missing PASSED [ 54%]
tests/test_flight_service.py::TestUpdateFlight::test_updates_provided_fields PASSED [ 57%]
tests/test_flight_service.py::TestUpdateFlight::test_updates_multiple_fields PASSED [ 59%]
tests/test_flight_service.py::TestUpdateFlight::test_leaves_unset_fields_unchanged PASSED [ 61%]
tests/test_flight_service.py::TestUpdateFlight::test_persists_update_in_store PASSED [ 64%]
tests/test_flight_service.py::TestUpdateFlight::test_returns_none_when_missing PASSED [ 66%]
tests/test_flight_service.py::TestUpdateFlight::test_update_preserves_flight_id PASSED [ 69%]
tests/test_flight_service.py::TestUpdateFlight::test_update_seats_available_only PASSED [ 71%]
tests/test_flight_service.py::TestDeleteFlight::test_deletes_existing_flight PASSED [ 73%]
tests/test_flight_service.py::TestDeleteFlight::test_returns_false_when_missing PASSED [ 76%]
tests/test_flight_service.py::TestDeleteFlight::test_delete_twice_returns_false PASSED [ 78%]
tests/test_flight_service.py::TestDeleteFlight::test_delete_leaves_other_flights_intact PASSED [ 80%]
tests/test_flight_service.py::TestDeleteFlight::test_delete_then_get_returns_none PASSED [ 83%]
tests/test_flights.py::test_create_flight PASSED                         [ 85%]
tests/test_flights.py::test_list_flights PASSED                          [ 88%]
tests/test_flights.py::test_search_flights_by_origin PASSED              [ 90%]
tests/test_flights.py::test_get_flight PASSED                            [ 92%]
tests/test_flights.py::test_get_flight_not_found PASSED                  [ 95%]
tests/test_flights.py::test_update_flight PASSED                         [ 97%]
tests/test_flights.py::test_delete_flight PASSED                         [100%]

=============================== warnings summary ===============================
../usr/local/lib/python3.12/site-packages/fastapi/testclient.py:1
  /usr/local/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

../usr/local/lib/python3.12/site-packages/starlette/testclient.py:53
  /usr/local/lib/python3.12/site-packages/starlette/testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 42 passed, 2 warnings in 0.19s ========================
```

## Constraints Observed

- No application source files under `app/` were modified.
- No test files under `tests/` were modified.
- No test configuration was added or changed (the suite still has no pytest config file).
- No dependencies were installed or upgraded.
- No changes were committed or merged. The only file written by this task is this report, `docs/task-2/test-report.md`.
