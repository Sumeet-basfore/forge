# Global Safety & Security Rules (`rules/safety.md`)

These rules protect system integrity, sensitive credentials, user data, and production infrastructure.

---

## 1. Destructive Operations

1. **No Silent Overwrites**:
   - Operations that discover existing project metadata (such as `.forge/`) or existing source files **MUST NEVER** silently replace or destroy them.
   - Destructive file deletions, directory resets, or database drops **MUST** require explicit human confirmation.
2. **Path Containment**:
   - File writes and executions **MUST** remain strictly within the designated repository directory tree.
   - Operations **MUST NOT** modify user home directories, global system configurations, or unrelated repositories.

---

## 2. Secrets & Credentials Management

1. **Zero Credentials in Repositories**:
   - API keys, tokens, passwords, private keys, database connection strings, and certificates **MUST NEVER** be committed to source control or written to task plan files.
   - Sensitive environment files (e.g., `.env`, `credentials.json`, `id_rsa`) **MUST** be listed in `.gitignore`.
2. **Zero Secrets in Logs**:
   - Test suites, CLI tools, and logging adapters **MUST NOT** print credentials, auth headers, or private keys to stdout, stderr, or log files.

---

## 3. External Systems & Network Boundaries

1. **No Unauthorized Network Requests**:
   - Automated tools and test suites **MUST NOT** send outbound network requests or exfiltrate codebase data to third-party endpoints without explicit user intent and authorization.
   - Tests **MUST** use local mocks or isolated loopback transports rather than reaching external internet services.

---

## 4. Release & Production Authority

1. **Mandatory Human Sign-Off**:
   - Releases, package publishing to registries (e.g., crates.io, PyPI, npm), and production deployments **MUST NOT** be executed without explicit, documented human authorization.
   - Agents **MUST NOT** autonomously publish or deploy code under any circumstance.
