# Testing Skill (`testing`)

## Purpose
Rigorously verify system correctness, validate edge cases, prevent regressions, and prove specification compliance through automated unit, integration, and property tests.

---

## When to Use
- Writing tests alongside or immediately following code implementation.
- Reproducing reported bugs with a failing test before applying a fix.
- Validating non-regression across the entire repository before code review and task completion.

---

## Required Context
- Task plan and acceptance criteria.
- Implemented code changes and modified interfaces.
- Test runner commands and configuration (e.g., `cargo test`, `pytest`, `npm test`).
- Existing test suites and fixture conventions.

---

## Procedure

1. **Identify Test Coverage Gaps**:
   - Map each acceptance criterion from the task plan to at least one test case.
   - Identify critical failure paths, malformed inputs, boundary values, and state transitions.

2. **Author Focused Unit Tests**:
   - Write tests close to the unit of logic (e.g., in `mod tests` or dedicated test modules).
   - Test happy path behavior, error returns, and boundary conditions.
   - Ensure test assertions validate concrete state and structured outputs, not merely boolean success.

3. **Author Integration & End-to-End Tests**:
   - Validate cross-module interactions and real data flows.
   - Test with realistic sample inputs, mock external transports/APIs if necessary, and verify proper error propagation.

4. **Ensure Test Quality & Hygiene**:
   - Tests must be deterministic (no flaky sleeps, race conditions, or unseeded random generators).
   - Tests must be isolated and side-effect free (use temporary directories, clean up database tables/resources).
   - Test names must clearly describe the scenario and expected outcome.

5. **Execute Full Suite Verification**:
   - Run unit tests for the modified component: `test_cmd` (scoped).
   - Run the full workspace test suite to verify zero regressions across unrelated crates/packages: `test_cmd` (workspace).
   - Fix any failures immediately in the implementation code; never adjust a test assertion to mask a real bug.

---

## Constraints
- **Never weaken assertions**: Do not lower thresholds, comment out assertions, or delete failing tests to make the suite green.
- **No flaky tests**: Avoid hardcoded timing thresholds (`sleep(100ms)`); use deterministic synchronizations or polling with timeouts.
- **Fast execution**: Unit tests should execute in milliseconds; integration tests must complete within reasonable toolchain timeouts.

---

## Outputs
- Comprehensive, clean test cases added to unit and integration test suites.
- Full test suite execution logs proving 100% pass rate.

---

## Verification
- All new tests pass.
- All pre-existing workspace tests pass (zero regressions).
- Linters on test targets pass with zero warnings (`--all-targets`).

---

## Stop Conditions
- All task acceptance criteria have passing automated test coverage and the entire workspace test suite passes with 0 failures.
