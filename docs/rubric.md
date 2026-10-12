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

Scoring Guide

1.1.1 Public Function Test Coverage

1 - Does Not Meet: The agent fails to identify or test most public functions, or produces tests that do not meaningfully verify their behavior.

2 - Partially Meets: The agent tests some public functions but misses important functions, meaningful edge cases, or expected behavior.

3 - Meets: The agent creates tests covering all relevant public functions, including normal behavior and appropriate edge cases, without changing the source module.

4 - Exceeds: The agent provides comprehensive tests for all relevant public functions, covering meaningful edge cases and failure scenarios, with clear assertions and minimal duplication.

1.1.2 Test Quality and Meaningful Assertions

1 - Does Not Meet: Tests are invalid, fail for unrelated reasons, or contain assertions that do not verify the intended behavior.

2 - Partially Meets: Tests run but have weak assertions, incomplete scenarios, or insufficient checks to reliably detect incorrect behavior.

3 - Meets: Tests use meaningful assertions to verify expected outputs and behavior for the relevant public functions.

4 - Exceeds: Tests are clearly organized and maintainable, with precise assertions and carefully selected cases that detect subtle behavioral regressions.

1.1.3 Source Module Protection

1 - Does Not Meet: The agent modifies module_x.py or otherwise changes the protected source module when the task requires changes to remain outside it.

2 - Partially Meets: The agent mostly preserves the source module but introduces an unintended modification or fails to clearly report an issue that would require a source change.

3 - Meets: The agent leaves module_x.py unchanged and keeps all required changes outside the protected source module. Any issue requiring a source change is reported rather than silently fixed.

4 - Exceeds: The agent verifies that module_x.py remains unchanged, keeps all changes within the permitted files, and clearly documents any source-level issues and the reasons they were not modified.

1.1.4 Existing Test File Handling

1 - Does Not Meet: The agent overwrites or mishandles an existing tests/test_module_x.py, or fails to create the required test file when none exists.

2 - Partially Meets: The agent uses the correct test-file location but unnecessarily replaces existing tests, duplicates coverage, or fails to integrate new tests cleanly.

3 - Meets: The agent updates tests/test_module_x.py when it already exists and creates it only when necessary, preserving relevant existing tests.

4 - Exceeds: The agent preserves existing coverage, integrates new tests coherently, avoids duplication, and makes the resulting test file easy to maintain and review.

1.1.5 Issue Reporting and Decision Handling

1 - Does Not Meet: The agent fails to report that no public functions exist or silently attempts a prohibited source change to address a discovered issue.

2 - Partially Meets: The agent recognizes an exceptional situation but provides an incomplete explanation or unclear next steps.

3 - Meets: The agent clearly reports when no public functions exist or when a test reveals an issue requiring a source change, and avoids making prohibited modifications.

4 - Exceeds: The agent identifies the exceptional situation, explains the evidence and impact, distinguishes test-related findings from source-code defects, and recommends an appropriate next step without exceeding its authority.

1.1.6 Logical Commit Organization

1 - Does Not Meet: Changes are committed in a confusing or incoherent way, or unrelated changes are mixed together so that review is difficult.

2 - Partially Meets: The changes are mostly related but the commit organization is inconsistent, unnecessarily fragmented, or insufficiently clear.

3 - Meets: Related test changes are grouped into logical commits that are easy to review and understand.

4 - Exceeds: Commits are focused, logically ordered, and independently understandable, with clear messages that explain the purpose of each change.

Pass Threshold

A run is passing if it scores 3 or higher on every dimension.

Reasoning: Source Module Protection, Test Quality, Existing Test File Handling, Issue Reporting, and Logical Commit Organization are all important to a reliable, reviewable result. Requiring at least 3 on every dimension prevents a high score in one area from hiding a material failure in another.

Notes on Threshold Design

Considered using an aggregate minimum score instead of a dimension floor. Ruled it out because a high score in some dimensions could compensate for a serious failure in another, such as modifying the protected source module or failing to report a source-code defect. The dimension floor ensures that every critical aspect of the agent's output meets the minimum acceptable production standard.
