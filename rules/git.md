# Global Git & Version Control Rules (`rules/git.md`)

These rules govern all Git operations and repository interactions.

---

## 1. Branching & Isolation

1. **No Direct Main Commits**:
   - Commits **MUST NOT** be made directly to the primary release branch (`main` / `master`) during normal task execution.
   - All work **MUST** be performed on dedicated task branches (e.g., `forge/<TASK_ID>` or `feature/<name>`).
2. **Clean Starting Baseline**:
   - A task branch **MUST** be created from a clean, up-to-date primary branch commit.
   - Working trees **MUST** be clean before switching branches or starting a task.

---

## 2. Diff Hygiene & Scope Containment

1. **Line-by-Line Diff Audit**:
   - The developer/agent **MUST** inspect `git diff` line by line before submitting work for review or closeout.
   - Diffs **MUST NOT** contain unintended formatting churn, trailing whitespace noise, debug statements, or scratch files.
2. **No Unrelated Edits**:
   - Diffs **MUST** only contain changes strictly necessary for the active task.
   - Unsolicited refactoring or opportunistic cleanups in unrelated modules **MUST NOT** be bundled with feature/fix commits.

---

## 3. Commit Discipline

1. **Logical & Atomic Commits**:
   - Commits **MUST** represent cohesive, atomic units of work that leave the repository in a compiling, testable state.
2. **Conventional Commit Messages**:
   - Commit messages **MUST** follow clear conventional formatting (e.g., `feat(subsystem): description`, `fix(subsystem): description`, `test(subsystem): description`).
   - Commit messages **MUST** explain *what* and *why*, not merely restate the diff.

---

## 4. Safe Repository Operations

1. **No Destructive Operations**:
   - `git push --force` or `--force-with-lease` **MUST NOT** be executed on shared or primary branches.
   - `git reset --hard` or `git clean -fd` **MUST NOT** be executed without explicit human confirmation.
2. **Untracked & Transient Artifacts**:
   - Build outputs, temporary logs, cache directories, and transient artifacts **MUST** be ignored in `.gitignore` and **MUST NOT** be committed to Git.
