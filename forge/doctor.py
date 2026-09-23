"""Environment and workspace diagnostics for Forge."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import shutil
import subprocess
import sys
from typing import List, Optional
import yaml

FORGE_ROOT = Path(__file__).resolve().parent.parent


class CheckStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    category: str
    name: str
    status: CheckStatus
    message: str
    details: Optional[str] = None


@dataclass
class DoctorReport:
    checks: List[CheckResult]

    @property
    def overall_status(self) -> CheckStatus:
        if any(c.status == CheckStatus.FAIL for c in self.checks):
            return CheckStatus.FAIL
        if any(c.status == CheckStatus.WARN for c in self.checks):
            return CheckStatus.WARN
        return CheckStatus.PASS


def _check_command_available(cmd: str) -> Optional[str]:
    """Return version string if command is executable, else None."""
    if not shutil.which(cmd):
        return None
    try:
        res = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if res.returncode == 0:
            return (res.stdout or res.stderr).strip().splitlines()[0]
    except Exception:
        pass
    return "Available"


def _check_project_toolchain(language: str, checks: List[CheckResult]) -> None:
    """Check toolchain presence for the detected project language."""
    lang_clean = language.strip().lower()
    if lang_clean == "rust":
        cargo_ver = _check_command_available("cargo")
        if cargo_ver:
            checks.append(
                CheckResult(
                    category="Project Toolchain",
                    name="Rust Toolchain (cargo)",
                    status=CheckStatus.PASS,
                    message=cargo_ver,
                )
            )
        else:
            checks.append(
                CheckResult(
                    category="Project Toolchain",
                    name="Rust Toolchain (cargo)",
                    status=CheckStatus.WARN,
                    message="cargo executable not found in PATH for Rust project",
                )
            )
    elif lang_clean == "python":
        py_tool = _check_command_available("python3") or _check_command_available("python")
        if py_tool:
            checks.append(
                CheckResult(
                    category="Project Toolchain",
                    name="Python Toolchain",
                    status=CheckStatus.PASS,
                    message=py_tool,
                )
            )
        else:
            checks.append(
                CheckResult(
                    category="Project Toolchain",
                    name="Python Toolchain",
                    status=CheckStatus.WARN,
                    message="python3 executable not found in PATH",
                )
            )
    elif lang_clean in {"typescript", "javascript", "node"}:
        node_ver = _check_command_available("node")
        if node_ver:
            checks.append(
                CheckResult(
                    category="Project Toolchain",
                    name="Node Runtime",
                    status=CheckStatus.PASS,
                    message=node_ver,
                )
            )
        else:
            checks.append(
                CheckResult(
                    category="Project Toolchain",
                    name="Node Runtime",
                    status=CheckStatus.WARN,
                    message="node executable not found in PATH for TypeScript/JavaScript project",
                )
            )


def run_doctor(
    project_path: Optional[Path] = None,
    forge_root: Optional[Path] = None,
) -> DoctorReport:
    """Run non-destructive environment, installation, and project diagnostics."""
    root = forge_root if forge_root is not None else FORGE_ROOT
    checks: List[CheckResult] = []

    # 1. Python Runtime
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 11):
        checks.append(
            CheckResult(
                category="Runtime",
                name="Python Version",
                status=CheckStatus.PASS,
                message=f"Python {py_ver} (>= 3.11 requirement satisfied)",
            )
        )
    else:
        checks.append(
            CheckResult(
                category="Runtime",
                name="Python Version",
                status=CheckStatus.FAIL,
                message=f"Python {py_ver} is unsupported. Forge requires Python >= 3.11",
            )
        )

    # 2. Git CLI
    git_ver = _check_command_available("git")
    if git_ver:
        checks.append(
            CheckResult(
                category="Runtime",
                name="Git CLI",
                status=CheckStatus.PASS,
                message=git_ver,
            )
        )
    else:
        checks.append(
            CheckResult(
                category="Runtime",
                name="Git CLI",
                status=CheckStatus.FAIL,
                message="git executable not found in PATH",
            )
        )

    # 3. Forge Core Directories
    skills_dir = root / "skills"
    if not skills_dir.exists():
        checks.append(
            CheckResult(
                category="Forge Environment",
                name="Skills Directory",
                status=CheckStatus.FAIL,
                message=f"Missing skills directory at {skills_dir}",
            )
        )
    else:
        skills = [p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
        if skills:
            checks.append(
                CheckResult(
                    category="Forge Environment",
                    name="Skills Directory",
                    status=CheckStatus.PASS,
                    message=f"Found {len(skills)} skills ({', '.join(s.name for s in skills)})",
                )
            )
        else:
            checks.append(
                CheckResult(
                    category="Forge Environment",
                    name="Skills Directory",
                    status=CheckStatus.WARN,
                    message=f"Skills directory exists at {skills_dir} but contains no SKILL.md files",
                )
            )

    rules_dir = root / "rules"
    if not rules_dir.exists():
        checks.append(
            CheckResult(
                category="Forge Environment",
                name="Rules Directory",
                status=CheckStatus.FAIL,
                message=f"Missing rules directory at {rules_dir}",
            )
        )
    else:
        rules = [p for p in rules_dir.iterdir() if p.is_file() and p.suffix == ".md"]
        if rules:
            checks.append(
                CheckResult(
                    category="Forge Environment",
                    name="Rules Directory",
                    status=CheckStatus.PASS,
                    message=f"Found {len(rules)} global rules ({', '.join(r.name for r in rules)})",
                )
            )
        else:
            checks.append(
                CheckResult(
                    category="Forge Environment",
                    name="Rules Directory",
                    status=CheckStatus.WARN,
                    message=f"Rules directory exists at {rules_dir} but contains no .md rule files",
                )
            )

    templates_dir = root / "templates"
    if not templates_dir.exists():
        checks.append(
            CheckResult(
                category="Forge Environment",
                name="Templates Directory",
                status=CheckStatus.FAIL,
                message=f"Missing templates directory at {templates_dir}",
            )
        )
    else:
        templates = [
            p for p in templates_dir.iterdir()
            if p.is_dir() and (p / ".forge" / "config.yaml").is_file()
        ]
        if templates:
            checks.append(
                CheckResult(
                    category="Forge Environment",
                    name="Templates Directory",
                    status=CheckStatus.PASS,
                    message=f"Found {len(templates)} templates ({', '.join(t.name for t in templates)})",
                )
            )
        else:
            checks.append(
                CheckResult(
                    category="Forge Environment",
                    name="Templates Directory",
                    status=CheckStatus.WARN,
                    message=f"Templates directory exists at {templates_dir} but contains no valid templates",
                )
            )

    projects_dir = root / "projects"
    if projects_dir.exists() and projects_dir.is_dir():
        checks.append(
            CheckResult(
                category="Forge Environment",
                name="Projects Directory",
                status=CheckStatus.PASS,
                message=f"Projects directory present at {projects_dir}",
            )
        )
    else:
        checks.append(
            CheckResult(
                category="Forge Environment",
                name="Projects Directory",
                status=CheckStatus.WARN,
                message=f"Projects directory not found at {projects_dir}",
            )
        )

    # 4. Target Project Diagnostics (if project_path passed or cwd is a project)
    target_project = project_path
    if target_project is None:
        cwd = Path.cwd()
        if (cwd / ".forge" / "config.yaml").is_file():
            target_project = cwd

    if target_project is not None:
        p_path = Path(target_project).resolve()
        if not p_path.exists():
            checks.append(
                CheckResult(
                    category="Project",
                    name="Project Directory",
                    status=CheckStatus.FAIL,
                    message=f"Specified project directory does not exist: {p_path}",
                )
            )
        else:
            # Check .forge/config.yaml
            config_file = p_path / ".forge" / "config.yaml"
            if not config_file.is_file():
                checks.append(
                    CheckResult(
                        category="Project",
                        name="Project Configuration",
                        status=CheckStatus.FAIL,
                        message=f"Missing .forge/config.yaml at {p_path}",
                    )
                )
            else:
                try:
                    raw_cfg = yaml.safe_load(config_file.read_text(encoding="utf-8"))
                    if isinstance(raw_cfg, dict):
                        proj_sec = raw_cfg.get("project", {}) if isinstance(raw_cfg.get("project"), dict) else {}
                        proj_name = proj_sec.get("name") or raw_cfg.get("name") or p_path.name
                        proj_lang = proj_sec.get("language") or raw_cfg.get("language") or raw_cfg.get("primary_language")
                        checks.append(
                            CheckResult(
                                category="Project",
                                name="Project Configuration",
                                status=CheckStatus.PASS,
                                message=f"Valid config for '{proj_name}' (language: {proj_lang or 'unspecified'})",
                            )
                        )

                        # Toolchain verification
                        if proj_lang:
                            _check_project_toolchain(proj_lang, checks)
                    else:
                        checks.append(
                            CheckResult(
                                category="Project",
                                name="Project Configuration",
                                status=CheckStatus.FAIL,
                                message="Invalid .forge/config.yaml: root must be a YAML mapping",
                            )
                        )
                except Exception as ex:
                    checks.append(
                        CheckResult(
                            category="Project",
                            name="Project Configuration",
                            status=CheckStatus.FAIL,
                            message=f"Failed to parse .forge/config.yaml: {ex}",
                        )
                    )

            # Check Git Repository Status
            try:
                git_check = subprocess.run(
                    ["git", "rev-parse", "--is-inside-work-tree"],
                    cwd=p_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if git_check.returncode == 0 and git_check.stdout.strip() == "true":
                    checks.append(
                        CheckResult(
                            category="Project",
                            name="Git Status",
                            status=CheckStatus.PASS,
                            message="Project is inside an active Git worktree",
                        )
                    )
                else:
                    checks.append(
                        CheckResult(
                            category="Project",
                            name="Git Status",
                            status=CheckStatus.WARN,
                            message="Project is not initialized as a Git repository",
                        )
                    )
            except Exception:
                checks.append(
                    CheckResult(
                        category="Project",
                        name="Git Status",
                        status=CheckStatus.WARN,
                        message="Unable to verify Git status for project",
                    )
                )

    return DoctorReport(checks=checks)
