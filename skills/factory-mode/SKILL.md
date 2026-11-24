---
name: factory-mode
description: "Run a change through your own factory: route the intent to Forge's procedures, drive the tasks through Forge Mate, and land through the factory gate. Use for /factory-mode, 'factory mode', or when you want a change routed rather than improvised."
---

# Factory mode

Run one task through the pipeline instead of improvising. Route the intent, let Forge Mate
schedule and verify the work, and land it through the check.

## The one invariant

A task's `verification:` list is copied from the target repo's `factory` block in its
`AGENTS.md`. Never invent it, never write it from memory. Forge Mate runs those commands
independently after the worker exits, and the same commands run on GitHub. One list, two
places, no drift.

Find the block, or write it first and run `bin/context-doctor --repos <name>` until it passes.
`bin/verify <repo>` runs the block locally and returns a receipt id.

## Routes

Pick a route from the request. Announce it in one line and proceed.

| intent | tasks | chain |
| --- | --- | --- |
| investigation | SCOUT | `research` |
| feature | SCOUT if the shape is unclear, then SHIP | `specification`, `planning`, `architecture`, `implementation`, `testing`, `code-review` |
| bug fix | SCOUT to find the mechanism, then SHIP | `research`, `testing` (failing test first), `implementation`, `code-review` |
| refactor | SHIP | `architecture`, `implementation`, `testing`, `code-review` |

Each route ends the same way, and that is the point of having routes at all. The task is not
done when the worker reports. It is done when the verification commands pass and the pull
request is merged with the `factory` check green.

Read the procedure for each step before writing the task document. Forge lives at
`/home/sumeet/personal-repo/projects/forge`, and procedures are at
`<forge>/skills/<name>/SKILL.md`, for example `<forge>/skills/planning/SKILL.md`. Do not restate
them here.

`worker.md` in this folder is the operator contract for a dispatched worker. Mate's
`contract.py` generates its own prompt today and does not read that file, so paste its rules into
a task's brief until it does.

## Procedure

1. Restate the goal and the route in one line. If the request is ambiguous in a way that changes
   the scope, ask once, with the specific fork.
2. Check the integration branch. Protected branches cannot take a local merge, so the cycle runs
   on its own branch.

   ```sh
   git switch -c factory/<slug>
   ```

3. Create the task documents in `.forge/tasks/<ID>.md` per `<forge>/skills/orchestration/SKILL.md`. SHIP
   tasks need `allowed_paths` kept as narrow as the work allows, and `verification` copied from
   the `factory` block.
4. Dispatch and drain.

   ```sh
   .venv/bin/python -m forge mate start --path .
   .venv/bin/python -m forge mate status --path .
   ```

   Call it as a module, not as `forge`. An unrelated `forge` AI shell is installed globally and
   answers to that name, and in this project's venv the console script has a stale shebang. The
   module form works in both places.

5. Read every review. `.venv/bin/python -m forge mate review <TASK_ID> --path .` shows the diff, the
   verification output, and the report. Check the diff yourself against the brief. A passing
   verification is necessary, not sufficient.
6. Accept, then merge into the integration branch.

   ```sh
   .venv/bin/python -m forge mate accept <TASK_ID> --path .
   .venv/bin/python -m forge mate merge <TASK_ID> --base-branch factory/<slug> --path .
   ```

7. Gate the integration branch and land it.

   ```sh
   ../../bin/verify .        # from /home/sumeet/personal-repo, bin/verify <repo>
   git push -u origin factory/<slug>
   gh pr create --fill
   ```

   The `factory` check decides. A red check is reported, never bypassed. Merging with a failing
   check is not a judgement call.

## Delegation

Forge Mate dispatches Codex workers itself. Start them with `mate start` and end your turn. Do
not spawn your own subagent for the same unit, and do not drive a worker's terminal.

- Model comes from `.forge/config.yaml`, key `codex.model`. With no key, the codex CLI config
  decides, which on this machine is `gpt-6-luna`.
- SCOUT runs read-only, SHIP runs `workspace-write`. Both are enforced in `forge/mate/codex.py`.
- A worker's own claim about tests is not evidence. Only the verification run counts.

## Reply

The route, the tasks and their statuses, the verification result per task, the PR, and the
receipt id. Name anything the route skipped and why.
