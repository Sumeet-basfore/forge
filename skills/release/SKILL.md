# Release Skill (`release`)

## Purpose
Prepare, validate, package, tag, and publish a project release with accurate version bumps, comprehensive changelog generation, build artifact verification, and explicit human authorization.

---

## When to Use
- Cutting a new formal release (patch, minor, or major version) from the main branch.
- Publishing packages to registries, container registries, or binary distributions.
- Preparing release candidate artifacts for pre-release validation.

---

## Required Context
- Target release version and bump type (Major, Minor, Patch) following Semantic Versioning (SemVer).
- Commit history since the previous release tag.
- Project manifest files containing version metadata (e.g., `Cargo.toml`, `pyproject.toml`, `package.json`).
- Release checklist, target registries, and distribution requirements.

---

## Procedure

1. **Pre-Release Cleanliness & Integrity Check**:
   - Verify that Git is on the primary release branch (`main`) and up-to-date.
   - Verify that the working tree is completely clean (`git status`).
   - Run full workspace verification (all tests, linters, doc-tests, and release-mode builds) to ensure zero failures.

2. **Determine Version & Semantic Impact**:
   - Inspect commits since previous tag:
     - **Major** (breaking API changes or architectural overhauls).
     - **Minor** (new backwards-compatible features).
     - **Patch** (backwards-compatible bug fixes and optimizations).
   - Ensure the proposed version number strictly follows SemVer.

3. **Update Version Metadata**:
   - Bump version numbers in project manifests and workspace lockfiles.
   - Update internal version constants or build identifiers if applicable.

4. **Compile Changelog**:
   - Update `CHANGELOG.md` following standard format (e.g., Keep a Changelog):
     - Added (new features)
     - Changed (changes in existing functionality)
     - Deprecated (soon-to-be removed features)
     - Removed (now removed features)
     - Fixed (bug fixes)
     - Security (vulnerabilities addressed)
   - Ensure every user-facing change has a concise, clear description.

5. **Build & Validate Release Artifacts**:
   - Build production release binaries, wheels, tarballs, or packages in release mode.
   - Verify package integrity, binary execution, and artifact checksums.

6. **Human Release Sign-Off (MANDATORY)**:
   - Present the release summary, version bump diff, and changelog to the human owner.
   - **DO NOT PROCEED WITHOUT EXPLICIT HUMAN APPROVAL.**

7. **Tag & Publish**:
   - Upon explicit human approval:
     - Commit version bump and changelog: `chore(release): vX.Y.Z`.
     - Create annotated git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
     - Publish artifacts or push tags according to project distribution procedure.

---

## Constraints
- **Absolute Human Authority**: Never publish a release, push a release tag, or deploy to production without explicit human sign-off.
- **No Dirty Releases**: Never tag or release from a dirty working tree or unmerged task branch.
- **Zero Test Failures**: Release verification must pass 100% with zero warnings/failures.

---

## Outputs
- Version bump commit updating manifest files and lockfiles.
- Updated `CHANGELOG.md`.
- Validated release artifacts (binaries, packages, checksums).
- Annotated Git release tag (`vX.Y.Z`).

---

## Verification
- Release build succeeds in release mode with optimizations.
- All workspace tests and linters pass cleanly.
- Manifest versions match the release tag exactly.
- Human approval is explicitly confirmed.

---

## Stop Conditions
- Release commit is created, annotated tag is generated, and release distribution is confirmed by the human owner.
