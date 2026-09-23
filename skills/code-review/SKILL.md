# Code Review Skill (`code-review`)

## Purpose
Perform objective, evidence-based, and thorough evaluations of proposed code changes against safety, correctness, architecture, maintainability, style, and scope boundaries prior to task sign-off or merging.

---

## When to Use
- After implementation and test verification are complete for a task.
- Before approving a task, pull request, or closeout operation.
- Conducting self-review or peer review of engineering artifacts.

---

## Required Context
- Task plan (`.forge/tasks/<TASK_ID>.md`) and allowed paths.
- Base branch and complete `git diff` against base.
- Verification and test execution results.
- Project coding rules (`rules/engineering.md`, `rules/safety.md`, `rules/git.md`).

---

## Procedure

1. **Scope & Diff Audit**:
   - Run `git diff <base_branch>...HEAD --stat` and inspect every modified file.
   - Verify 100% adherence to declared `allowed_paths`. Flag any out-of-scope edits as immediate blockers.
   - Check diff size: ensure no unnecessary refactoring, formatting churn, or accidental whitespace edits.

2. **Correctness & Robustness Review**:
   - Check algorithm logic, off-by-one errors, boundary conditions, and overflow/underflow risks.
   - Verify proper error handling: are errors propagated cleanly or handled gracefully? Are there any unhandled unwraps/panics in production paths?
   - Verify resource management: are file handles, sockets, database locks, and memory buffers safely closed/released?

3. **Architecture & API Consistency**:
   - Verify that changes conform to existing system patterns, naming conventions, and module boundaries.
   - Ensure public API modifications are minimal, backward-compatible, and well-documented.
   - Check for unwanted circular dependencies or architectural layer violations.

4. **Test & Verification Coverage**:
   - Verify that all new logic and edge cases have dedicated test coverage.
   - Ensure existing tests were not weakened, disabled, or deleted.
   - Confirm that full workspace tests and linters pass cleanly.

5. **Generate Review Report**:
   - Synthesize findings into a structured review report:
     - **Summary**: Objective and key changes.
     - **Diff Analysis**: Files modified and line statistics.
     - **Verification Status**: Test and linter results.
     - **Findings & Observations**: Categorized into *Critical*, *Improvements*, and *Notes*.
     - **Verdict**: `APPROVE`, `REQUEST CHANGES`, or `REJECT` with specific rationales.

6. **Present to Human Reviewer**:
   - Surface the review report for human decision.
   - The human owner remains the ultimate authority on task approval.

---

## Constraints
- Review must be factual and grounded in exact file paths and line numbers.
- Do not rubber-stamp changes without inspecting the full diff.
- Coding agents must never self-approve or bypass human review for critical tasks.

---

## Outputs
- Structured review report document (`.forge/reviews/REV-<TASK_ID>.md` or response summary) containing:
  - Exact diff statistics.
  - Verification checklist status.
  - Critical issues or defects found (if any).
  - Explicit review recommendation and human decision.

---

## Verification
- All findings cite exact line ranges and reproducible scenarios.
- Recommendation is consistent with verification results and scope constraints.

---

## Stop Conditions
- Review report is complete, clear, and presented to the human owner for final decision.
