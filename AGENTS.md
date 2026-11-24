# Forge

Rules for agents working in this repo. `rules/` holds the invariants, `skills/` holds the
procedures, `templates/` holds the starting points for new projects. Read `README.md` before
changing the tool.

## Gate

Every change runs the suite before it lands.

```factory
test: uv run --extra dev python -m pytest -q
```

`bin/verify .` from `/home/sumeet/personal-repo` runs it and writes a receipt. Name the
receipt id when you report.

## House rules

- Skills are prose, and prose that does not change a decision gets deleted. Each `SKILL.md`
  names its own procedure and points at other skills by path rather than restating them.
- A new mate command gets a test in `tests/mate/`. The suite is the contract.
- Codex workers run read-only for SCOUT and `workspace-write` for SHIP. Do not widen either.
- Do not weaken a test assertion to make a change pass.

## Layout

```
forge/          the CLI and the mate scheduler, gates, worktrees, verification
rules/          global invariants for agents, engineering, git, safety
skills/         procedural skills, including factory-mode and orchestration
templates/      per-stack project scaffolds with .forge/config.yaml
tests/          mate and unit suites, pytest
```
