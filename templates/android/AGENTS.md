# Agent Guidelines for {{ project_name }}

This project follows Forge engineering conventions.

## 1. Toolchain Commands
- **Build**: `./gradlew assembleDebug`
- **Test**: `./gradlew test`
- **Lint**: `./gradlew lint`
- **Format**: `./gradlew spotlessCheck`

## 2. Project Documentation
- Architecture overview: `docs/architecture.md`
- Contribution standards: `docs/contributing.md`
- Forge project metadata: `.forge/config.yaml`
- Task specifications: `.forge/tasks/`

## 3. Forge Rules & Skills Reference
All modifications must conform to Forge global rules:
- `rules/engineering.md`: Code quality, tests, dependencies, zero warnings.
- `rules/agents.md`: Autonomy limits, context handling, no fabricated APIs.
- `rules/git.md`: Branch hygiene, clean diffs, no unrelated changes.
- `rules/safety.md`: Credential safety, explicit human authorization.

Refer to Forge procedural skills under `skills/` (`planning`, `implementation`, `testing`, `code-review`).

## 4. Core Agent Invariants
1. **Inspect Before Modifying**: Understand existing manifest configurations, Gradle plugins, and Android components.
2. **Bounded Scope**: Make the smallest coherent change necessary for the task.
3. **No Unrelated Changes**: Do not touch files outside the task scope.
4. **No Fabricated APIs**: Rely strictly on verified Android SDK APIs and established libraries.
5. **Mandatory Verification**: Run `./gradlew assembleDebug` and `./gradlew test` before declaring task completion.
6. **Human Authority**: The human developer owns architecture, acceptance, and release decisions.
