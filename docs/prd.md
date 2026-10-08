This workflow creates unit tests for all public functions in module_x.py without modifying the source module.
Trigger: A developer manually invokes the coding agent with the prompt "Write unit tests for module_x.py." from the repository root.
The workflow is initiated manually; there is no automated trigger.


Agent 1: Writes unit tests for module_x.py.

Prompt: Write unit tests for module_x.py.

- Create tests/test_module_x.py

- Cover all public functions

- Do not modify module_x.py itself

- Commit in logical chunks


Decision Events

- If module_x.py contains public functions, the agent creates tests covering those functions.

- If module_x.py contains no public functions, the agent reports that there are no public functions to test.

- If tests/test_module_x.py already exists, the agent updates the existing test file rather than creating a duplicate file.

- If writing or running the tests reveals an issue that would require modifying module_x.py, the agent does not modify module_x.py and reports the issue.


Actions

1. Read module_x.py to identify all public functions.

2. Create the tests/ directory if it does not already exist.

3. Create tests/test_module_x.py.

4. Write unit tests for all public functions in module_x.py.

5. Run the relevant test suite to verify that the tests execute successfully.

6. Review the test results and identify any failures or issues.

7. If the tests reveal an issue that requires changing module_x.py, leave module_x.py unchanged and report the issue.

8. Commit the test changes in logical chunks.

Acceptance Criteria

- tests/test_module_x.py exists.
- Every public function in module_x.py has at least one corresponding unit test.
- module_x.py is unchanged after the workflow completes.
- The tests in tests/test_module_x.py run successfully.
- Any test failures or issues discovered during the test run are reported.
- Changes are committed in logical chunks.





