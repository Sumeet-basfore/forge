# Architecture Skill (`architecture`)

## Purpose
Design high-level subsystem boundaries, component responsibilities, state models, data flow pipelines, and technical trade-offs that satisfy specifications while keeping system complexity minimal.

---

## When to Use
- Designing new subsystems or major modules.
- Restructuring or decoupling existing components.
- Deciding data storage, communication protocols, state management, or concurrency models.
- Evaluating architectural alternatives and documenting Architectural Decision Records (ADRs).

---

## Required Context
- Approved feature or system specification.
- Existing codebase architecture, modularity guidelines, and dependency rules.
- Non-functional requirements (performance, memory, scalability, platform constraints).
- Language idioms and framework best practices.

---

## Procedure

1. **Analyze System Constraints & Goals**:
   - Review specification requirements and identify key architectural drivers (e.g., latency, simplicity, isolation, testability).

2. **Define Component Boundaries & Ownership**:
   - Partition functionality into cohesive components with single responsibilities.
   - Establish strict interface boundaries between components to minimize coupling.
   - Define data ownership: which component is the single source of truth for each piece of state?

3. **Model Data Flow & State Lifecycle**:
   - Trace end-to-end data flow through components.
   - Design state transitions, lifecycle events, and synchronization mechanisms.
   - Explicitly define error propagation, recovery strategies, and failure domain boundaries.

4. **Evaluate Trade-offs & Alternatives**:
   - Compare at least two viable architectural approaches.
   - Assess each option against the Forge simplicity principle: prefer simpler local designs over complex distributed or layered abstractions.

5. **Document Architecture & Decisions (ADR)**:
   - Author an ADR or architecture guide (`docs/architecture/` or `.forge/decisions/`):
     - **Context**: The problem and forces at play.
     - **Decision**: Chosen architecture and components.
     - **Rationale**: Why this design was chosen over alternatives.
     - **Consequences**: Positive effects, trade-offs, and technical debt incurred.
     - **Component Diagrams**: ASCII or Mermaid diagrams visualizing relationships.

6. **Seek Alignment**:
   - Present the architecture and ADR to the human owner for review and sign-off.

---

## Constraints
- Apply the **Principle of Minimal Necessary Complexity**: do not add layers, plugins, generic wrappers, microservices, or complex state machines without concrete, immediate necessity.
- Do not violate established language idioms or project-wide dependency rules.
- Do not begin code implementation until architectural direction is agreed upon.

---

## Outputs
- Architecture document or ADR (`docs/architecture/<system>.md` or `docs/adr/<NNN-title>.md`) containing:
  - System topology and component boundaries.
  - Data flow diagrams and lifecycle state models.
  - Interface definitions and trait/type hierarchies.
  - Rationale and evaluated alternatives.

---

## Verification
- Every component has a single, well-defined responsibility.
- State ownership is unambiguous with no circular dependencies or race conditions.
- Architecture directly fulfills all specification requirements.
- Human owner has reviewed and approved the architecture.

---

## Stop Conditions
- Architectural design is thoroughly documented, verified against constraints, and approved by the human owner.
