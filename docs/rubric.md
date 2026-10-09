### 1.1.1 Public Function Coverage

Measures how completely the generated tests cover all public functions in `module_x.py`. A high score requires every public function to have appropriate tests for normal behavior, edge cases, and relevant error conditions.

### 1.1.2 Test Correctness and Reliability

Measures whether the generated tests correctly verify the intended behavior of the public functions. A high score requires meaningful assertions, appropriate test inputs, and reliable execution.

### 1.1.3 Source Module Preservation

Measures whether the agent respects the requirement not to modify `module_x.py`. A high score requires all changes to remain outside the source module and any issues requiring source changes to be reported.

### 1.1.4 Existing Test File Handling

Measures whether the agent handles existing test files correctly. A high score requires updating `tests/test_module_x.py` if it already exists and creating it only when necessary.

### 1.1.5 Issue Reporting and Decision Handling

Measures whether the agent correctly handles exceptional situations. A high score requires reporting when no public functions exist or when a test reveals an issue that would require modifying `module_x.py`.

### 1.1.6 Logical Commit Organization

Measures how effectively the agent organizes changes into logical commits. A high score requires related test changes to be grouped coherently and made easy to review.

## 1.2 Alternatives Considered

An alternative was to use a binary pass/fail checklist for each acceptance criterion. This was ruled out because it cannot distinguish partial test coverage from comprehensive coverage or identify which aspects of the agent's work need improvement.
