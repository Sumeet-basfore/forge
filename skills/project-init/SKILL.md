# Project Initialization Skill (`project-init`)

## Purpose
Establish a clean, consistent, and reproducible project environment with standardized conventions, configuration, documentation, and version control.

---

## When to Use
- Creating a new project from scratch.
- Bootstrapping a project from a standard template.
- Onboarding an existing repository to Forge engineering conventions.

---

## Required Context
- Target project name and workspace directory.
- Target primary language/runtime (e.g., Rust, Python, TypeScript, Go).
- Project category (CLI application, library, service, frontend).
- Any existing source files, license preferences, or user-supplied requirements.

---

## Procedure

1. **Workspace Safety Check**:
   - Inspect the target directory.
   - If an existing `.forge/` configuration or git repository is present, **never** silently overwrite it.
   - Verify that target paths do not conflict with existing files.

2. **Establish Directory Hierarchy**:
   - Create the standard project layout:
     ```text
     <project-root>/
       ├── .forge/
       │   ├── config.yaml
       │   ├── tasks/
       │   ├── decisions/
       │   └── reviews/
       ├── docs/
       ├── src/ (or language-standard source root)
       ├── tests/
       ├── AGENTS.md
       └── README.md
     ```

3. **Configure Project Metadata**:
   - Generate `.forge/config.yaml` specifying:
     - Project name, language, and version.
     - Toolchain commands (`build_cmd`, `test_cmd`, `lint_cmd`, `format_cmd`).
     - Default policies and paths.
   - Create or update `.gitignore` with standard language and toolchain ignores, plus `.forge/` transient paths.

4. **Initialize Documentation**:
   - Create `README.md` with project overview, architecture summary, and quickstart instructions.
   - Create `AGENTS.md` defining project-specific conventions, directory layout, commands, and rules for coding agents.
   - Initialize `docs/` with starter architecture and design guides.

5. **Toolchain & Dependency Bootstrap**:
   - Initialize the language package manifest (e.g., `Cargo.toml`, `pyproject.toml`, `package.json`).
   - Configure linter, formatter, and test runner configurations matching project standards.
   - Add a minimal hello-world / smoke-test entry point to verify the toolchain.

6. **Baseline Verification**:
   - Run the project build command.
   - Run the project test command.
   - Run the project linter / formatter check.

7. **Initial Git Commit**:
   - Initialize git repository if not already initialized.
   - Stage all initial files and create the baseline commit: `feat: initial project scaffold`.

---

## Constraints
- Never overwrite existing project files, configurations, or Git history without explicit human approval.
- Keep templates and initial files minimal; do not install unnecessary frameworks or bloat.
- Toolchain commands in `.forge/config.yaml` must be runnable from the repository root.

---

## Outputs
- Standardized directory layout.
- Valid `.forge/config.yaml` with executable toolchain commands.
- Informative `AGENTS.md` and `README.md`.
- Working language package manifest and buildable entry point.
- Clean initial Git commit on the main branch.

---

## Verification
- `build_cmd` succeeds with zero errors.
- `test_cmd` succeeds with zero failures.
- `lint_cmd` succeeds with zero warnings.
- `git status` reports a clean working tree.

---

## Stop Conditions
- Project is fully initialized, baseline tests pass, git working tree is clean, and the environment is ready for task planning.
