# Rubric — Task 2

Score each dimension from 1 to 4.

| Dimension | 1 — Does Not Meet | 2 — Partially Meets | 3 — Meets | 4 — Exceeds |
|---|---|---|---|---|
| Test Execution | Command not executed | Incorrect/incomplete execution | Correct command executed | Correct execution with exit status and evidence |
| Result Accuracy | Incorrect results | Significant omissions | Accurate counts and status | Accurate counts, warnings, and detailed findings |
| Report Quality | Missing report | Incomplete report | Clear, complete report | Highly structured and reproducible report |
| Source Protection | Unauthorized changes | Unclear modification scope | No source/test changes | Git diff confirms preservation |
| Evidence | No supporting evidence | Limited evidence | Command and output recorded | Full terminal evidence retained |
| Git Commit | No commit | Incomplete/unrelated commit | Relevant files committed | Focused, well-described commit |

## Pass Threshold
Every dimension must score at least 3/4.

A failing test suite does not automatically fail the workflow if the failures are accurately reported.
