# Specification Skill (`specification`)

## Purpose
Define precise, unambiguous functional and non-functional requirements, data contracts, interface definitions, and verifiable acceptance criteria for a system change before design or implementation.

---

## When to Use
- Starting a new feature, protocol, API, or data model change.
- Refactoring critical subsystems where behavior invariants must be preserved.
- Translating ambiguous user requests into concrete engineering requirements.
- Establishing formal contracts between multiple components or services.

---

## Required Context
- High-level user request or product goal.
- Research findings and existing system behavior.
- Domain rules, security boundaries, and performance constraints.
- Existing data models and API contracts.

---

## Procedure

1. **Define Scope Boundaries**:
   - Explicitly list what is **IN SCOPE**.
   - Explicitly list what is **OUT OF SCOPE** to prevent scope creep.

2. **Specify Functional Requirements**:
   - Detail every user-visible and system-visible behavior.
   - Describe inputs, valid formats, outputs, and transformations.
   - Define exact error conditions, error codes, and failure modes.
   - Specify boundary conditions and edge cases (e.g., empty inputs, unicode, extreme values, timeouts).

3. **Define Data Contracts & Interfaces**:
   - Specify data schemas, wire formats, serialization rules, and field constraints.
   - Document invariants that must hold true before and after operations.
   - Define API method signatures, return types, and exceptions/errors.

4. **Define Non-Functional Requirements**:
   - Specify performance targets (latency, memory footprint, throughput).
   - Detail concurrency, safety, and compatibility requirements (e.g., backwards compatibility with older data versions).

5. **Formulate Falsifiable Acceptance Criteria**:
   - Write clear Given-When-Then or itemized acceptance criteria.
   - Every criterion must be objectively testable via automated tests or concrete manual checks.

6. **Review & Align**:
   - Present the specification document (`docs/specs/<feature>.md`) to the human owner.
   - Resolve any ambiguities or conflicts before proceeding to architecture/planning.

---

## Constraints
- Focus strictly on **WHAT** the system must do, not how internal code will be implemented.
- Do not invent speculative requirements; keep the specification grounded in immediate needs.
- Never proceed to implementation with unresolved requirement contradictions.

---

## Outputs
- Specification document (`docs/specs/<feature>.md`) containing:
  - Background & Objective
  - Scope (In-Scope / Out-of-Scope)
  - Functional Requirements & Edge Cases
  - Data Models & API Contracts
  - Non-Functional Requirements
  - Acceptance Criteria Checklist

---

## Verification
- Every acceptance criterion is unambiguous, falsifiable, and directly verifiable.
- Specification is verified against existing domain invariants and approved by the human owner.

---

## Stop Conditions
- Specification is complete, all questions/ambiguities are resolved, and the human owner has approved the requirements.
