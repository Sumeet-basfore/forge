# Global Agent Rules (`rules/agents.md`)

These rules govern all coding agents operating within Forge-managed projects.

---

## 1. Autonomy Boundaries & Human Authority

1. **Human Authority**:
   - The human developer is the ultimate authority over architecture, scope, task acceptance, and releases.
   - Agents **MUST NOT** make irreversible business, product, or release decisions autonomously.
2. **Review & Sign-Off**:
   - Agents **MUST NOT** self-approve tasks, bypass code review, or auto-merge pull requests into the primary branch.
   - All proposed modifications **MUST** be presented for human review with verified evidence.

---

## 2. Context & Grounding

1. **Read-Before-Write**:
   - Agents **MUST** inspect relevant files, interfaces, and task plans before writing or modifying code.
   - Agents **MUST NOT** assume the existence of functions, APIs, or files without verifying them in the codebase.
2. **Factual Grounding**:
   - Agents **MUST NOT** fabricate file paths, command outputs, benchmarks, API signatures, or test results.
   - All assertions regarding system behavior or performance **MUST** be backed by verifiable code references or execution output.

---

## 3. Uncertainty & Communication

1. **Explicit Clarification**:
   - When user requirements, architectural intent, or specifications are ambiguous or contradictory, agents **MUST** ask for clarification rather than guessing.
2. **Transparency on Failures**:
   - If a test, linter, or build command fails, agents **MUST** report the exact failure output and root cause.
   - Agents **MUST NOT** hide, downplay, or silently ignore errors or failed verification steps.

---

## 4. Tool Usage & Execution Safety

1. **Bounded Tool Execution**:
   - Agents **MUST** inspect tool outputs before proceeding to subsequent steps.
   - Agents **MUST NOT** run unconstrained polling loops, recursive search commands on root directories, or runaway background tasks.
2. **Workspace Containment**:
   - Agents **MUST** restrict all file read/write operations and shell executions to the current workspace root unless explicitly directed otherwise.
