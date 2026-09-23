# Contributing to {{ project_name }}

## Development Workflow
1. Create a task branch (`forge/<TASK_ID>`).
2. Follow Forge engineering principles and project guidelines in `AGENTS.md`.
3. Implement bounded changes with corresponding tests.
4. Verify toolchain checks (`cargo check`, `cargo test`, `cargo clippy`, `cargo fmt`).
5. Submit for human review and approval.

## Code Standards
- Keep changes minimal, coherent, and verified.
- Do not introduce unrelated modifications or unapproved dependencies.
- Maintain zero compiler or clippy warnings.
