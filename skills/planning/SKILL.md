# Planning Skill (`planning`)

## Purpose
Deconstruct specifications and architectural designs into a series of bounded, sequenced, incrementally testable tasks with explicit scope constraints, file boundaries, and verification criteria.

---

## When to Use
- Before writing or modifying code for any feature, refactor, performance optimization, or non-trivial bug fix.
- Organizing complex multi-step engineering initiatives into safe, incremental units of work.

---

## Required Context
- Approved specification and/or architecture document.
- Current codebase state, active branch, and directory tree.
- Project toolchain commands from `.forge/config.yaml` or project manifest.
- Allowed file paths and scope constraints.

---

## Procedure

1. **Define Task Scope & ID**:
   - Assign a unique task identifier (e.g., `TASK-001`, `TASK-002`).
   - Define a concise objective statement.
   - Enumerate strict `allowed_paths` for the task (only files that need modification).

2. **Identify Invariants & Preconditions**:
   - Note key domain invariants that must remain unbroken (e.g., backward compatibility, zero regression on existing tests).
   - Verify that the base branch and working tree are clean before planning execution.

3. **Break Down Incremental Steps**:
   - Sequence steps logically from foundational data structures to high-level integration:
     - Step 1: Core models / data structures.
     - Step 2: Internal logic / parsing / algorithms.
     - Step 3: Public API exposure / trait implementation.
     - Step 4: Unit and integration tests.
     - Step 5: Documentation updates.
   - Ensure each step is small enough to reason about and independently testable.

4. **Define Concrete Verification Checks**:
   - For every step, specify exact verification commands (e.g., `cargo test -p my-crate --lib`, `cargo clippy`, `npm test`).
   - Define expected observable outcomes.

5. **Risk Assessment & Rollback**:
   - Identify potential failure modes, performance impacts, or API breaking risks.
   - Specify mitigation or rollback steps.

6. **Generate Task Plan File**:
   - Write the plan into `.forge/tasks/<TASK_ID>.md` (or `.forge/plans/<TASK_ID>.md`) using the standard plan template:
     - Objective
     - Scope & Allowed Paths
     - Step-by-step Implementation Plan
     - Verification Commands
     - Acceptance Criteria Checklist

7. **Seek Human Plan Approval**:
   - Present the plan to the human owner for review before starting implementation.

---

## Constraints
- Never plan unbounded changes that modify arbitrary files across the entire codebase in a single task.
- Stay strictly within the scope agreed in the specification.
- Every step must have a concrete, executable verification method.

---

## Outputs
- Structured task plan file (`.forge/tasks/<TASK_ID>.md`) containing:
  - Task metadata (ID, title, branch name, allowed paths).
  - Background & objectives.
  - Step-by-step technical plan with file paths.
  - Test and verification checklist.
  - Explicit acceptance criteria.

---

## Verification
- Allowed paths cover all files needed for the task without unnecessary extras.
- Verification commands are valid and executable in the current environment.
- Plan is reviewed and approved by the human owner.

---

## Stop Conditions
- Task plan is documented, validated, approved by the human owner, and ready for execution.
