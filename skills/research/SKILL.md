# Research Skill (`research`)

## Purpose
Investigate codebases, dependencies, external APIs, protocols, architectural patterns, or bug root causes to build factual, evidence-based context before making design decisions or modifying code.

---

## When to Use
- Requirements, problem domains, or unfamiliar algorithms require clarification.
- Diagnosing a complex bug or unexpected behavior before attempting fixes.
- Evaluating third-party libraries, protocols, or external integrations.
- Assessing performance bottlenecks, compatibility concerns, or migration paths.

---

## Required Context
- Specific research question(s) or problem statement.
- Target repository or subsystem paths.
- Relevant documentation, RFCs, issue reports, or specification references.
- Operational constraints (e.g., supported platforms, language versions, license constraints).

---

## Procedure

1. **Formulate Concrete Research Questions**:
   - Define exact, falsifiable questions (e.g., "How does subsystem X handle reconnects?", "What is the memory overhead of library Y?").
   - Identify what decisions depend on the answers.

2. **Codebase Exploration (Read-Only)**:
   - Trace control flow, data models, call graphs, and type hierarchies related to the questions.
   - Inspect test cases to understand expected behavior and existing edge-case handling.
   - Grep for relevant keywords, symbols, error codes, and configuration flags.

3. **External & Domain Investigation**:
   - Read official documentation, RFCs, specs, and reference implementations.
   - Check changelogs, open issues, and known pitfalls for relevant dependencies.
   - When benchmarking, create isolated scratch benchmarks to collect empirical data.

4. **Synthesize Findings & Trade-offs**:
   - Summarize factual findings directly tied to code references (file paths and line numbers).
   - Enumerate potential solutions or approaches with pros, cons, and risks.
   - Highlight potential edge cases, migration risks, and breaking changes.

5. **Document Research Summary**:
   - Record findings in a structured Markdown research note (e.g., `docs/research/<topic>.md` or in the task context).
   - Provide concrete, actionable recommendations for the specification/planning phase.

---

## Constraints
- Research is strictly **read-only** with respect to the project's source tree. Do not modify production code, refactor files, or add dependencies during research.
- Do not make unsubstantiated claims; always cite specific source files, lines, or official documentation.
- Do not make architectural or product commitments without human concurrence.

---

## Outputs
- Research notes containing:
  - Answers to all initial research questions.
  - Code references (file paths, functions, data structures).
  - Comparative analysis of viable approaches with trade-offs.
  - Concrete recommendations and risks.

---

## Verification
- Every claim in the research summary is backed by verified code, test output, or official documentation links.
- Working tree remains completely unmodified (`git status` is clean).

---

## Stop Conditions
- Research questions are comprehensively answered with sufficient clarity to proceed to specification or planning.
