# Implementation Skill (`implementation`)

## Purpose
Execute precise, high-quality, bounded source code modifications strictly conforming to an approved task plan and project engineering invariants.

---

## When to Use
- Active coding phase of an approved task plan.
- Implementing features, bug fixes, performance improvements, or refactors.

---

## Required Context
- Approved task plan (`.forge/tasks/<TASK_ID>.md`).
- Target repository working directory.
- `allowed_paths` defined in the plan.
- Project coding standards, conventions, and `.forge/config.yaml` toolchain commands.

---

## Procedure

1. **Pre-Implementation Check**:
   - Verify that Git is on the correct task branch (e.g., `forge/<TASK_ID>`).
   - Verify working tree is clean and baseline builds/tests pass before touching code.
   - Re-read the task plan to understand all constraints and step requirements.

2. **Incremental Step Execution**:
   - Implement changes step-by-step following the plan.
   - Strictly restrict modifications to files within `allowed_paths`.
   - Adhere to idiomatic language patterns, error handling conventions, and memory/type safety rules.
   - Preserve existing documentation comments, docstrings, and formatting in untouched sections of code.

3. **Defensive Coding & Edge Cases**:
   - Handle edge cases, null/none values, empty collections, and error conditions explicitly.
   - Do not use unbounded loops, unchecked unwraps, or panics in production logic unless explicitly required.
   - Ensure clean resource release (file handles, network sockets, memory buffers).

4. **Continuous Local Verification**:
   - Run local compilation/build checks frequently during editing.
   - Run language linters (`clippy`, `eslint`, `ruff`, etc.) to catch issues immediately.
   - Fix any introduced compiler warnings or lint errors before moving to the next step.

5. **Self-Review & Diff Inspection**:
   - Run `git diff` to inspect all modifications line by line.
   - Verify that no unintended edits, debug print statements, scratch files, or formatting churn were introduced.
   - Verify that all changes directly map to the approved task plan.

---

## Constraints
- **Strict Scope Boundary**: Never modify files outside `allowed_paths`. If an unexpected file modification is required, pause and update the plan first with explicit justification.
- **No Unapproved Dependencies**: Do not add new external libraries or packages without explicit plan authorization.
- **Documentation Integrity**: Maintain and update inline API comments for any added or modified functions and types.
- **No Test Weakening**: Never weaken, disable, or delete existing tests to force a pass.

---

## Outputs
- Clean, idiomatic, compiling source code changes satisfying all planned steps.
- Maintained or updated inline docstrings and module documentation.
- Clean diff adhering 100% to `allowed_paths`.

---

## Verification
- Code compiles and builds cleanly (`0` compilation errors).
- Linters pass with `0` warnings/errors (`cargo clippy`, `npm run lint`, `ruff check`).
- `git diff --stat` confirms only allowed paths were modified.

---

## Stop Conditions
- All code changes outlined in the task plan are implemented, compiling cleanly, lint-free, and ready for testing.
