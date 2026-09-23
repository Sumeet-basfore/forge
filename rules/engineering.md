# Global Engineering Rules (`rules/engineering.md`)

These rules are project invariants. They apply to all code modifications across all projects and languages.

---

## 1. Code Quality & Standards

1. **Compilation & Lint Cleanliness**:
   - Code **MUST** compile and build cleanly with zero compiler, interpreter, or type-checker errors.
   - Code **MUST** pass all project linters with zero warnings and zero errors (`-D warnings` / zero lint violations).
2. **Defensive Error Handling**:
   - Code **MUST** handle error cases, null/none values, and boundary conditions explicitly.
   - Code **MUST NOT** use unchecked panics, unhandled unwraps, or empty catch blocks in production paths.
3. **Idioms & Consistency**:
   - Code **MUST** conform to standard idioms and existing patterns of the target language and codebase.
   - Code **MUST** preserve existing formatting conventions; do not reformat untouched blocks.

---

## 2. Scope Discipline

1. **Declared Path Boundaries**:
   - Changes **MUST** remain strictly within the declared `allowed_paths` of the active task plan.
   - Changes **MUST NOT** modify unrelated files, configurations, or modules.
2. **No Scope Creep**:
   - Changes **MUST NOT** introduce speculative features, unused abstractions, or unrequested refactors.
   - If an unexpected file modification is necessary, the task plan **MUST** be updated and justified before editing that file.

---

## 3. Test Discipline

1. **Zero Test Weakening**:
   - Existing tests **MUST NOT** be deleted, disabled, commented out, or weakened to make a build pass.
   - Assertions **MUST NOT** be made less strict without explicit human justification and sign-off.
2. **Deterministic & Isolated**:
   - Tests **MUST** be deterministic and independent; tests **MUST NOT** rely on hardcoded `sleep` durations or unseeded randomness.
   - Tests **MUST** clean up temporary files, database rows, or network bindings created during execution.
3. **Regression Prevention**:
   - Every bug fix **MUST** be accompanied by a regression test reproducing the issue.
   - The entire workspace test suite **MUST** pass with 100% success before completing any task.

---

## 4. Dependency Management

1. **Minimal Dependencies**:
   - New third-party dependencies **MUST NOT** be added without explicit plan justification and human approval.
   - Standard library solutions **MUST** be preferred over external packages for simple utility logic.
2. **Licensing & Security**:
   - Dependencies **MUST** use permissible open-source licenses (MIT, Apache-2.0, BSD).
   - Dependencies **MUST NOT** introduce known security vulnerabilities or deprecated upstream packages.

---

## 5. Maintainability & Documentation

1. **Documentation Integrity**:
   - Public APIs, traits, structs, functions, and configuration options **MUST** have accurate docstrings.
   - Existing comments and docstrings in untouched code **MUST** be preserved.
2. **No Dead Code**:
   - Code **MUST NOT** introduce commented-out code blocks, orphaned functions, or unused imports.
