# Forge (v0.2)

> **A reusable personal software factory consisting of Skills, Rules, Templates, and Project Context that helps coding agents perform software development consistently.**

---

## 1. What Forge Is

Forge is a lightweight, stateless, file-based developer tool designed for solo software engineers pairing with coding agents. It establishes clear engineering boundaries, reproducible workflows, and consistent project conventions across diverse programming languages and codebases.

### Core Model
```text
Forge
  ├── Skills     (procedural workflows: planning, implementation, testing, code-review...)
  ├── Rules      (global invariants: engineering, agents, git, safety)
  ├── Templates  (reusable project scaffolds: rust, python, typescript, android)
  └── Projects   (independent Git repositories with .forge/ metadata and AGENTS.md)
```

---

## 2. What Forge Is NOT

- **NOT an Agent Runner or Swarm**: Forge does not spawn or execute LLMs or subprocess agents.
- **NOT an Orchestration or CI Engine**: Forge does not run background daemons or automated deployment pipelines.
- **NOT a Database-Backed State Machine**: No `.forge/state.yaml`, task databases, or hidden runtime caches.
- **NOT an Autonomous System**: The human engineer retains complete authority over product architecture, scope, acceptance, and releases.

---

## 3. Installation

Forge requires Python `>= 3.11` and Git.

```bash
# Clone and install locally
git clone https://github.com/your-username/forge.git ~/forge
cd ~/forge
pip install -e .
```

---

## 4. CLI Commands

```bash
# 1. Scaffold a new project from a template
forge new <name> --template <rust|python|typescript|android> [--path <dir>] [--force]

# 2. List available procedural skills
forge skills

# 3. Discover existing Forge projects
forge projects [--path <dir>]

# 4. Diagnose environment, toolchain, and project health
forge doctor [--path <dir>]

# 5. Assemble deterministic Markdown context for a coding agent
forge context [--skill <name>] [--task <task-spec>] [--path <project-dir>]
```

---

## 5. Skills (`skills/`)

Forge includes 10 standardized, procedural Markdown skills:

| Skill | Purpose |
| :--- | :--- |
| `project-init` | Establish a clean, reproducible project environment with baseline conventions. |
| `research` | Investigate codebases, dependencies, and APIs to build factual, evidence-based context. |
| `specification` | Define unambiguous functional requirements, data contracts, and acceptance criteria. |
| `architecture` | Design decoupled, modular system boundaries and data flow models. |
| `planning` | Deconstruct specifications into bounded, testable, and sequenced task plans. |
| `implementation` | Execute high-quality source code modifications conforming strictly to task scope. |
| `testing` | Validate correctness, edge cases, and regression safety through automated tests. |
| `code-review` | Objectively evaluate proposed code diffs against safety, correctness, and scope. |
| `documentation` | Maintain accurate, human-readable architecture and contributing guides. |
| `release` | Prepare, validate, package, tag, and publish software releases with human approval. |

---

## 6. Global Rules (`rules/`)

Non-negotiable invariants applied across all tasks and agent interactions:
- [`rules/engineering.md`](rules/engineering.md): Code quality, zero compiler/linter warnings, test discipline.
- [`rules/agents.md`](rules/agents.md): Read before write, bounded scope, no fabricated APIs, human authority.
- [`rules/git.md`](rules/git.md): Dedicated task branches, clean diff inspection, conventional commits.
- [`rules/safety.md`](rules/safety.md): Zero secrets, no destructive overwrites, explicit human authorization.

---

## 7. Templates (`templates/`)

Lightweight starting scaffolds with minimal toolchain definitions:
- **Rust** (`templates/rust`): Standard `Cargo.toml`, `src/main.rs`.
- **Python** (`templates/python`): Modern `pyproject.toml`, `src/`, `tests/` (`pytest`, `ruff`).
- **TypeScript** (`templates/typescript`): `package.json`, `tsconfig.json`, `src/`, `tests/` (ES2022 / NodeNext).
- **Android** (`templates/android`): Kotlin DSL Gradle configuration and manifest files.

---

## 8. Project Structure

Every Forge project remains a standard Git repository:

```text
my-project/
├── .git/
├── .forge/
│   ├── config.yaml          # Project identity & toolchain commands (build, test, lint, format)
│   └── tasks/               # Markdown task plans (TASK-001.md, ...)
├── docs/
│   ├── architecture.md      # Architectural structure & components
│   └── contributing.md      # Development workflow & standards
├── src/                     # Source code
├── AGENTS.md                # Agent boundaries & toolchain instructions
└── README.md
```

---

## 9. Example Workflow with an External Coding Agent

```text
1. Create a new project:
   forge new my-app --template rust

2. Create a bounded task plan in .forge/tasks/TASK-001.md

3. Assemble deterministic context:
   forge context --skill implementation --task TASK-001 --path . > /tmp/context.md

4. Provide context to your coding agent (e.g. Antigravity, Claude, Copilot)

5. Inspect diff line by line:
   git diff

6. Run verification:
   cargo test && cargo clippy --all-targets -- -D warnings

7. Human code review and standard Git commit:
   git add -p && git commit -m "feat: implement TASK-001"
```
