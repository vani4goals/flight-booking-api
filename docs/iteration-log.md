# Iteration Log

## Run 002 -- 2026-10-19 -- Baseline

### Task

Generate unit tests for `app/services/flight_service.py`. This is a second baseline run with the same prompt as Run 001, used to measure run-to-run variance.

### Full prompt

```text
Write unit tests for app/services/flight_service.py.
```

### Rubric Scores

Scored against [`docs/rubric.md`](rubric.md) with the same criteria and file mapping as Run 001 (scale: 1 = Does Not Meet, 2 = Partially Meets, 3 = Meets, 4 = Exceeds). Scores approved by the human reviewer on 2026-10-19; 1.1.3 and 1.1.5 were confirmed against the Run 002 session transcript (`87735f24-239e-49b1-aad6-f14d2444ceca`).

| # | Dimension | Score | Rationale |
|---|-----------|-------|-----------|
| 1.1.1 | Public Function Test Coverage | 4 | All 5 public `FlightService` methods have normal, edge, and missing-ID tests (13 / 3 / 5 / 11 / 5). The pre-existing destination-prefix case (`"LA"` vs `LAX`) was lost in the rewrite; counted under 1.1.4. |
| 1.1.2 | Test Quality and Meaningful Assertions | 4 | 37/37 targeted and 75/75 full-suite tests pass; precise assertions on zero-value updates, explicit `None`, copy semantics, and store independence. No coupling to `BookingService`. |
| 1.1.3 | Source Module Protection | 3 | `app/services/flight_service.py` unchanged. The transcript shows the agent read it before writing tests, but never verified afterwards that it was unchanged (Run 001 did, with `git diff --stat`). |
| 1.1.4 | Existing Test File Handling | 1 | The agent overwrote `tests/test_flight_service.py` with a single `Write`; all 29 existing tests were replaced, none by name preserved. The transcript shows it never knew the file existed. |
| 1.1.5 | Issue Reporting and Decision Handling | 3 | No exceptional situation arose and no prohibited change was made. The final summary said "I added" the file and did not disclose that 29 tests were replaced; it corrected a 36-to-37 miscount. |
| 1.1.6 | Logical Commit Organization | 2 | No commit was made, as in Run 001. |
| | **Total** | **17/24** | Lowest dimension: 1 (1.1.4) |

### Rubric Variance (Run 001 vs Run 002)

| Metric | Value |
|--------|-------|
| Run 001 rubric score | 21/24 |
| Run 002 rubric score | 17/24 |
| Variance | Run 002 scored 4 points lower |

| # | Dimension | Run 001 | Run 002 | Change |
|---|-----------|---------|---------|--------|
| 1.1.1 | Public Function Test Coverage | 4 | 4 | 0 |
| 1.1.2 | Test Quality and Meaningful Assertions | 4 | 4 | 0 |
| 1.1.3 | Source Module Protection | 4 | 3 | -1 |
| 1.1.4 | Existing Test File Handling | 4 | 1 | -3 |
| 1.1.5 | Issue Reporting and Decision Handling | 3 | 3 | 0 |
| 1.1.6 | Logical Commit Organization | 2 | 2 | 0 |

### Measurements

| Metric | Value | Source |
|--------|-------|--------|
| Cycle time | 2 minutes 35.931 seconds (155.931 seconds) | `time claude ...` (`real`) |
| Review latency | Not measured | No review start/end timestamps were recorded |
| Human review duration (retrospective) | 25 minutes | Reported by the reviewer, recorded 2026-10-19. This is the review's duration, not the review latency, which remains not measured. |
| Input tokens | 2,204 (Opus 5.5: 1,026; Haiku 5.5: 1,178) | Claude Code `cost-state` record, session `87735f24-239e-49b1-aad6-f14d2444ceca` |
| Output tokens | 4,594 (Opus 5.5: 4,577; Haiku 5.5: 17) | Claude Code `cost-state` record |
| Cache read / write tokens | 372,276 / 18,332 (Opus 5.5) | Claude Code `cost-state` record |
| Cost | $0.26 ($0.2618855) | Claude Code `cost-state` record (Claude Code's estimate, not a billing statement) |
| Generated tests | 37 in `tests/test_flight_service.py` | Agent's final summary; `python -m pytest tests/test_flight_service.py` |
| Targeted tests | 37 passed in 0.06 seconds | `python -m pytest tests/test_flight_service.py -v` |
| Full suite | 75 passed | `python -m pytest` |

The `cost-state` record covers the whole session, including the follow-up `pytest -v` turn the reviewer requested after the agent's first summary.

### Cycle Time Variance (Run 001 vs Run 002)

| Metric | Value |
|--------|-------|
| Run 001 cycle time | 3 minutes 15.352 seconds (195.352 seconds) |
| Run 002 cycle time | 2 minutes 35.931 seconds (155.931 seconds) |
| Absolute difference | 39.421 seconds |
| Percentage difference | 20.18% relative to Run 001 |

Run 002 completed 39.421 seconds faster than Run 001 (baseline), taking 20.18% less time with the same task prompt.

### Cost Variance (Run 001 vs Run 002)

| Metric | Run 001 | Run 002 | Difference |
|--------|---------|---------|------------|
| Cost | $0.3271111 | $0.2618855 | -$0.0652256 (19.94% lower) |
| Input tokens | 1,706 | 2,204 | +498 (29.19% higher) |
| Output tokens | 4,643 | 4,594 | -49 (1.06% lower) |
| Cache read tokens | 517,039 | 372,276 | -144,763 (27.99% lower) |
| Cache write tokens | 25,789 | 18,332 | -7,457 (28.92% lower) |

Both figures come from each session's Claude Code `cost-state` record and are Claude Code's estimates, not billing statements. Run 002 cost 19.94% less than Run 001, mainly because it read and wrote fewer cached tokens, consistent with its fewer discovery calls. Run 002's record also includes the reviewer-requested `pytest -v` follow-up turn.

### Environment differences from Run 001

Both runs started from commit `29a87ce` with the same prompt, the same `app/`, `tests/` and `requirements.txt`, the same 29 tests in `tests/test_flight_service.py`, no `CLAUDE.md`, and only `prd.md` and `rubric.md` in `docs/`. Known differences:

| # | Item | Run 001 | Run 002 |
|---|------|---------|---------|
| 1 | Claude Code version | 2.1.300 | 2.1.303 |
| 2 | Branch | `main` | `run-002-baseline` |
| 3 | Python packages | pytest not installed; the agent ran `pip install -q -r requirements.txt` during the run | Packages from Run 001's install kept; pytest already installed, and the agent ran no install step |
| 4 | `.pytest_cache`, `tests/__pycache__` | State as of Run 001 | Refreshed since Run 001 (gitignored) |
| 5 | Org-synced skills (`~/.claude/skills/synced`) | Pre-update | Updated 2026-10-19 (outside repo control) |

Difference 3 means part of the cycle-time reduction probably comes from the skipped dependency install rather than from run-to-run variance alone. Whether pluggy, iniconfig, Pygments, PyYAML, uvloop and watchfiles were absent before Run 001 or present at other versions cannot be confirmed.

### Variance note

Run 002 scored 4 points lower than Run 001 with the same prompt and starting commit. Almost all of the drop (3 of 4 points) is in 1.1.4. Run 001 extended the existing test file in place; Run 002 replaced it. The transcript shows why: the agent's discovery command, `ls -R app tests 2>/dev/null | head -50`, was cut off at 50 lines before `tests/test_flight_service.py` appeared, and the agent never read that file, so it wrote the file as if it were new. The `Write` tool accepted the overwrite and reported the file as "updated", which the agent did not act on. The remaining point is 1.1.3: Run 002 did not verify that the source module was unchanged after the run, while Run 001 did. Coverage and test quality were the same in both runs, and both runs failed to commit.

The faster cycle time should not be read as an improvement in agent efficiency. Run 002 skipped the dependency install Run 001 needed (environment difference 3) and made fewer discovery calls, including the skipped read of the existing test file. Other known differences are the Claude Code version (2.1.300 vs 2.1.303), the branch, refreshed gitignored caches, and updated org-synced skills. None of these can be ruled out as a cause of the behavioral difference, so with two runs this is recorded as run-to-run variance rather than attributed to a single cause.

Human review took 25 minutes for Run 002 and 30 minutes for Run 001, 5 minutes (16.7%) less. Both figures are durations reported by the reviewer, not timestamped measurements, and neither is review latency, which was not measured for either run. The two reviews also differed in method. Run 001's review was retrospective, completed days after the 2026-10-15 run. Run 002's review was assisted: an agent-prepared rubric evaluation and transcript analysis were reviewed and approved by the reviewer on the day of the run. The shorter duration may reflect that assistance and familiarity from reviewing Run 001 rather than an easier-to-review run, so the two durations are not directly comparable.

### Pass/Fail

**FAIL.** The rubric's pass threshold requires a score of 3 or higher on every dimension; 1.1.4 Existing Test File Handling scored 1 and 1.1.6 Logical Commit Organization scored 2.

### Observations

The agent overwrote `tests/test_flight_service.py` with a single `Write` call without first reading the existing file. Run 001 had extended the file in place. The 29 pre-existing tests were replaced rather than extended, so the file went from 29 to 37 tests. The agent did not commit its work. Its final summary corrected an earlier miscount (36) to 37 tests.

Transcript review (session `87735f24-239e-49b1-aad6-f14d2444ceca`): the agent read `app/services/flight_service.py` and `app/models/flight.py` before writing tests and ran the full suite afterwards. It did not run `git diff` or `git status` after writing. Its summary described the file as added, not replaced. `session_tasks.md` was not touched during the run: its working-tree diff is byte-for-byte identical to the pre-run backup, and its last modification (2026-10-03) predates all available transcripts, so who changed it cannot be determined.

### Changes made

None. This is a second baseline run with the Run 001 prompt.

## Run 001 -- 2026-10-15 -- Baseline

### Task

Generate unit tests for `app/services/flight_service.py`.

### Full prompt

```text
Write unit tests for app/services/flight_service.py.
```

### Rubric Scores

Scored against [`docs/rubric.md`](rubric.md) (scale: 1 = Does Not Meet, 2 = Partially Meets, 3 = Meets, 4 = Exceeds). The rubric's `module_x.py` / `tests/test_module_x.py` are read as `app/services/flight_service.py` / `tests/test_flight_service.py`.

| # | Dimension | Score | Rationale |
|---|-----------|-------|-----------|
| 1.1.1 | Public Function Test Coverage | 4 | All 5 public `FlightService` methods have normal, edge, and missing-ID tests; 13 tests added (29 → 42). |
| 1.1.2 | Test Quality and Meaningful Assertions | 4 | 42/42 targeted and 80/80 full-suite tests pass; assertions are precise and target subtle regressions (e.g. zero-value updates). |
| 1.1.3 | Source Module Protection | 4 | `app/services/flight_service.py` unchanged; the agent verified this with `git diff --stat` and reported no source defects. |
| 1.1.4 | Existing Test File Handling | 4 | Existing `tests/test_flight_service.py` extended in place; no tests removed or duplicated. |
| 1.1.5 | Issue Reporting and Decision Handling | 3 | No exceptional situation arose and none was misreported; final summary overstated tests added (claimed 15, actual 13). |
| 1.1.6 | Logical Commit Organization | 2 | No commit was made, so the PRD's "Commit in logical chunks" requirement was not met. |
| | **Total** | **21/24** | Lowest dimension: 2 (1.1.6) |

### Measurements

| Metric | Value | Source |
|--------|-------|--------|
| Cycle time | 3 minutes 15.352 seconds | `time claude ...` (`real`) |
| Review latency | Not measured | No review start/end timestamps were recorded |
| Human review duration (retrospective) | 30 minutes | Reported by the reviewer; a retrospective review completed after the run, recorded 2026-10-19. This is the review's duration, not the original review latency, which remains not measured. |
| Input tokens | 1,706 (Opus 5.5: 528; Haiku 5.5: 1,178) | Claude Code `cost-state` record, session `fcdc80bb-2651-4971-9d71-27a90bbce55e` |
| Output tokens | 4,643 (Opus 5.5: 4,626; Haiku 5.5: 17) | Claude Code `cost-state` record |
| Cache read / write tokens | 517,039 / 25,789 (Opus 5.5) | Claude Code `cost-state` record |
| Cost | $0.33 ($0.3271111) | Claude Code `cost-state` record (Claude Code's estimate, not a billing statement) |
| Targeted tests | 42 passed | `python -m pytest tests/test_flight_service.py -v` |
| Full suite | 80 passed | `python -m pytest -v` |

### Pass/Fail

**FAIL.** The rubric's pass threshold requires a score of 3 or higher on every dimension; 1.1.6 Logical Commit Organization scored 2.

### Observations

The agent noticed that `tests/test_flight_service.py` already existed and extended it from 29 to 42 tests without removing any. `app/services/flight_service.py` was left unchanged, and both the targeted suite (42 passed) and the full suite (80 passed) were green. The agent did not commit its work, which is the sole reason the run failed; the baseline prompt omitted the PRD's "Commit in logical chunks" instruction. The new `test_delete_leaves_existing_bookings_in_place` test depends on `BookingService`, coupling the flight-service tests to booking-service behavior. The agent's final summary claimed 15 tests were added when 13 were.

### Retrospective human review

A human reviewer completed a retrospective review of Run 001 lasting 30 minutes, recorded on 2026-10-19. It took place after the run, so it does not provide the original review latency (time from the agent finishing to review completion); that metric remains not measured. The baseline measurements above are unchanged. The 21/24 rubric score remains the original score; it is not recorded as human-validated because the review has not been confirmed to validate it.

### Changes made

None. This is the baseline run.
