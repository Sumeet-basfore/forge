# Documentation Skill (`documentation`)

## Purpose
Maintain clear, accurate, complete, and up-to-date documentation across project READMEs, architectural records, API docstrings, user manuals, and configuration references.

---

## When to Use
- Adding a new feature, CLI command, configuration parameter, or public API.
- Modifying existing system behavior, interfaces, or default settings.
- Creating onboarding materials, developer setup guides, or troubleshooting documents.
- Auditing existing documentation for staleness, broken links, or inaccuracies.

---

## Required Context
- Code changes, pull requests, or specification documents.
- Target audience (end users, library consumers, system administrators, or coding agents).
- Project documentation standards and Markdown conventions.
- Current documentation files (`README.md`, `docs/`, `AGENTS.md`, docstrings).

---

## Procedure

1. **Identify Documentation Impact**:
   - Trace all public-facing changes:
     - New/modified CLI commands or arguments.
     - New/modified configuration keys and default values in `.forge/config.yaml` or environment variables.
     - Public API methods, structs, types, error variants, and traits.
     - Changed workflows or installation prerequisites.

2. **Update Inline Code Documentation**:
   - Write or update docstrings for all exported types, functions, methods, and modules.
   - Include brief explanations of parameters, return values, error conditions, and example usage.
   - Preserve existing documentation comments that are unrelated to current edits.

3. **Update Architectural & Reference Guides**:
   - If architectural decisions were made, document them in `docs/architecture/` or `docs/decisions/`.
   - Update `docs/` guides with accurate code examples and sequence diagrams where beneficial.

4. **Update Project Guides & README**:
   - Ensure `README.md` reflects accurate feature lists, quickstart snippets, and usage examples.
   - Ensure `AGENTS.md` reflects current directory structures, toolchain commands, and agent guidelines.

5. **Validate Examples & Links**:
   - Test every documented command and code snippet to guarantee it works as written.
   - Verify that all relative Markdown links and image references are valid and resolve correctly.

---

## Constraints
- Never leave obsolete, contradictory, or placeholder documentation in published branches.
- Do not add verbose narrative filler; prefer clear headings, concise bullet points, and working code examples.
- Preserve existing documentation formatting conventions and style.

---

## Outputs
- Updated `README.md`, `AGENTS.md`, and relevant files in `docs/`.
- Thorough inline API docstrings on all modified/added public symbols.
- Accurate, working code snippets and command references.

---

## Verification
- All code snippets and CLI examples execute without error.
- All Markdown links resolve correctly without 404s.
- Linter / doc-tests (e.g., `cargo test --doc`) pass cleanly with zero failures.

---

## Stop Conditions
- Documentation accurately reflects current system behavior, all code examples are verified, and no broken links exist.
