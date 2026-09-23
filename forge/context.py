"""Deterministic Agent Context Assembler for Forge v0.2."""

from pathlib import Path
from typing import List, Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = FORGE_ROOT / "rules"
SKILLS_DIR = FORGE_ROOT / "skills"


def list_available_skills(skills_dir: Optional[Path] = None) -> List[str]:
    """Return a sorted list of available skill names."""
    s_dir = (skills_dir if skills_dir is not None else SKILLS_DIR).resolve()
    if not s_dir.exists() or not s_dir.is_dir():
        return []
    skills = [
        p.name
        for p in s_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").is_file()
    ]
    return sorted(skills)


def load_global_rules(rules_dir: Optional[Path] = None) -> str:
    """Load all global rule files in deterministic alphabetical order."""
    r_dir = (rules_dir if rules_dir is not None else RULES_DIR).resolve()
    if not r_dir.exists() or not r_dir.is_dir():
        raise FileNotFoundError(f"Global rules directory not found at: {r_dir}")

    rule_files = sorted(
        [p for p in r_dir.iterdir() if p.is_file() and p.suffix == ".md"],
        key=lambda p: p.name,
    )
    if not rule_files:
        return "## 1. Global Rules\n\nNo global rule files found in rules directory."

    chunks = ["## 1. Global Rules"]
    for rf in rule_files:
        content = rf.read_text(encoding="utf-8").strip()
        chunks.append(f"### rules/{rf.name}\n\n{content}")

    return "\n\n".join(chunks)


def load_skill(skill_name: str, skills_dir: Optional[Path] = None) -> str:
    """Load a specific skill definition by name with path traversal protection."""
    clean_skill = skill_name.strip().lower()
    if not clean_skill:
        raise ValueError("Skill name cannot be empty.")

    s_dir = (skills_dir if skills_dir is not None else SKILLS_DIR).resolve()
    if not s_dir.exists() or not s_dir.is_dir():
        raise FileNotFoundError(f"Skills directory not found at: {s_dir}")

    skill_folder = (s_dir / clean_skill).resolve()

    # Path traversal protection
    try:
        skill_folder.relative_to(s_dir)
    except ValueError:
        raise ValueError(f"Path traversal detected in skill name: '{skill_name}'")

    skill_file = skill_folder / "SKILL.md"
    if not skill_file.is_file():
        available = list_available_skills(s_dir)
        raise ValueError(
            f"Unknown skill '{skill_name}'. Available skills: {', '.join(available)}"
        )

    content = skill_file.read_text(encoding="utf-8").strip()
    return f"## 2. Skill\n\n### {clean_skill}\n\n{content}"


def load_project_context(project_dir: Path) -> str:
    """Load project metadata, conventions, and configuration deterministically."""
    p_dir = Path(project_dir).resolve()
    if not p_dir.exists() or not p_dir.is_dir():
        raise FileNotFoundError(f"Project directory not found: {p_dir}")

    chunks = ["## 3. Project Context"]

    # 1. .forge/config.yaml
    config_file = p_dir / ".forge" / "config.yaml"
    if config_file.is_file():
        config_text = config_file.read_text(encoding="utf-8").strip()
        chunks.append(f"### .forge/config.yaml\n\n```yaml\n{config_text}\n```")

    # 2. AGENTS.md
    agents_file = p_dir / "AGENTS.md"
    if agents_file.is_file():
        agents_text = agents_file.read_text(encoding="utf-8").strip()
        chunks.append(f"### AGENTS.md\n\n{agents_text}")

    # 3. docs/architecture.md
    arch_file = p_dir / "docs" / "architecture.md"
    if arch_file.is_file():
        arch_text = arch_file.read_text(encoding="utf-8").strip()
        chunks.append(f"### docs/architecture.md\n\n{arch_text}")

    if len(chunks) == 1:
        chunks.append("No project context files found (.forge/config.yaml, AGENTS.md, docs/architecture.md).")

    return "\n\n".join(chunks)


def load_task(task_spec: str, project_dir: Optional[Path] = None) -> str:
    """Resolve and load task content deterministically (file, task ID, or inline text)."""
    clean_spec = task_spec.strip()
    if not clean_spec:
        return "## 4. Task\n\nNo task specification provided."

    p_dir = Path(project_dir).resolve() if project_dir is not None else Path.cwd().resolve()

    # Candidate file resolution
    candidates = [
        Path(clean_spec),
        p_dir / clean_spec,
        p_dir / ".forge" / "tasks" / clean_spec,
        p_dir / ".forge" / "tasks" / f"{clean_spec}.md",
    ]

    for cand in candidates:
        if cand.is_file():
            content = cand.read_text(encoding="utf-8").strip()
            return f"## 4. Task\n\n### {clean_spec}\n\n{content}"

    # If it looks like a file path or task ID but wasn't found, fail clearly
    if clean_spec.endswith(".md") or clean_spec.startswith(".") or clean_spec.startswith("/") or clean_spec.startswith("TASK-"):
        checked_paths = [str(c) for c in candidates]
        raise FileNotFoundError(
            f"Task file for '{task_spec}' not found in project. Checked candidate locations: {checked_paths}"
        )

    # Otherwise treat as direct inline task text
    return f"## 4. Task\n\n{clean_spec}"


def assemble_context(
    skill: Optional[str] = None,
    task: Optional[str] = None,
    project_dir: Optional[Path] = None,
    rules_dir: Optional[Path] = None,
    skills_dir: Optional[Path] = None,
) -> str:
    """Assemble complete, deterministic agent context string.
    
    Order:
      1. GLOBAL RULES
      2. SKILL
      3. PROJECT CONTEXT
      4. TASK
    """
    p_dir = project_dir if project_dir is not None else Path.cwd()

    sections: List[str] = []

    # 1. Global Rules
    sections.append(load_global_rules(rules_dir))

    # 2. Skill
    if skill:
        sections.append(load_skill(skill, skills_dir))
    else:
        sections.append("## 2. Skill\n\nNo specific skill requested.")

    # 3. Project Context
    sections.append(load_project_context(p_dir))

    # 4. Task
    if task:
        sections.append(load_task(task, p_dir))
    else:
        sections.append("## 4. Task\n\nNo specific task requested.")

    header = "# Forge Agent Context\n\n"
    divider = "\n\n---\n\n"
    return header + divider.join(sections).strip() + "\n"
