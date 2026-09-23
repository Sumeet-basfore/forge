"""Dynamic discovery for Forge skills and projects."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import yaml

FORGE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILLS_DIR = FORGE_ROOT / "skills"
DEFAULT_PROJECTS_DIR = FORGE_ROOT / "projects"


@dataclass
class SkillInfo:
    name: str
    purpose: str
    path: Path


@dataclass
class ProjectInfo:
    name: str
    path: Path
    language: Optional[str] = None
    error: Optional[str] = None


def extract_skill_purpose(skill_file: Path) -> str:
    """Extract the purpose summary from a SKILL.md document."""
    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception:
        return "No description available (unable to read file)."

    lines = content.splitlines()
    in_purpose = False
    purpose_lines: List[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## Purpose"):
            in_purpose = True
            continue
        if in_purpose:
            if stripped.startswith("## ") or stripped.startswith("---"):
                break
            if stripped:
                purpose_lines.append(stripped)

    if purpose_lines:
        return " ".join(purpose_lines)
    return "No purpose specified."


def discover_skills(skills_dir: Optional[Path] = None) -> List[SkillInfo]:
    """Discover all available skills dynamically from the skills directory."""
    s_dir = skills_dir if skills_dir is not None else DEFAULT_SKILLS_DIR
    if not s_dir.exists() or not s_dir.is_dir():
        return []

    discovered: List[SkillInfo] = []
    for entry in sorted(s_dir.iterdir(), key=lambda p: p.name):
        if entry.is_dir() and not entry.name.startswith("."):
            skill_md = entry / "SKILL.md"
            if skill_md.is_file():
                purpose = extract_skill_purpose(skill_md)
                discovered.append(
                    SkillInfo(
                        name=entry.name,
                        purpose=purpose,
                        path=skill_md.resolve(),
                    )
                )

    return discovered


def discover_projects(projects_dir: Optional[Path] = None) -> List[ProjectInfo]:
    """Discover all Forge projects within a target projects directory."""
    p_dir = projects_dir if projects_dir is not None else DEFAULT_PROJECTS_DIR
    if not p_dir.exists() or not p_dir.is_dir():
        return []

    projects: List[ProjectInfo] = []
    for entry in sorted(p_dir.iterdir(), key=lambda p: p.name):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        config_path = entry / ".forge" / "config.yaml"
        if not config_path.is_file():
            continue

        try:
            content = config_path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                projects.append(
                    ProjectInfo(
                        name=entry.name,
                        path=entry.resolve(),
                        language=None,
                        error="Malformed configuration: root must be a YAML mapping.",
                    )
                )
                continue

            # Support both {project: {name: ..., language: ...}} and top-level fields
            proj_section = data.get("project", {}) if isinstance(data.get("project"), dict) else {}
            name = (
                proj_section.get("name")
                or data.get("name")
                or data.get("project_name")
                or entry.name
            )
            language = (
                proj_section.get("language")
                or data.get("language")
                or data.get("primary_language")
            )

            projects.append(
                ProjectInfo(
                    name=str(name),
                    path=entry.resolve(),
                    language=str(language) if language else None,
                )
            )
        except Exception as ex:
            projects.append(
                ProjectInfo(
                    name=entry.name,
                    path=entry.resolve(),
                    language=None,
                    error=f"Malformed configuration: {ex}",
                )
            )

    return projects
