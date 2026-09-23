"""Project scaffolding and template instantiation for Forge v0.2."""

import os
from pathlib import Path
import shutil
from typing import List, Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = FORGE_ROOT / "templates"
DEFAULT_PROJECTS_DIR = FORGE_ROOT / "projects"


def list_templates(templates_dir: Optional[Path] = None) -> List[str]:
    """Return a sorted list of available project template names."""
    t_dir = templates_dir if templates_dir is not None else TEMPLATES_DIR
    if not t_dir.exists():
        return []
    templates = [
        p.name
        for p in t_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / ".forge" / "config.yaml").exists()
    ]
    return sorted(templates)


def create_project(
    name: str,
    template: str,
    target_dir: Optional[Path] = None,
    force: bool = False,
    templates_dir: Optional[Path] = None,
) -> Path:
    """Instantiate a project from a template with strict conflict detection.
    
    Args:
        name: Name of the project.
        template: Template identifier (e.g. 'rust', 'python', 'typescript', 'android').
        target_dir: Target directory path. If None, defaults to Forge projects directory / name.
        force: If True, allows overwriting existing files in destination directory.
        templates_dir: Optional override path for template library.
        
    Returns:
        Path to the initialized project directory.
        
    Raises:
        ValueError: If name is empty or template is unrecognized.
        FileExistsError: If destination contains existing .forge metadata or files and force is False.
    """
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Project name cannot be empty.")

    template_key = template.strip().lower()
    t_dir = templates_dir if templates_dir is not None else TEMPLATES_DIR
    available = list_templates(t_dir)
    if template_key not in available:
        raise ValueError(
            f"Unknown template '{template}'. Available templates: {', '.join(available)}"
        )

    if target_dir is not None:
        dest = Path(target_dir).resolve()
    else:
        if DEFAULT_PROJECTS_DIR.exists():
            dest = (DEFAULT_PROJECTS_DIR / clean_name).resolve()
        else:
            dest = (Path.cwd() / clean_name).resolve()

    template_path = t_dir / template_key

    # Pre-flight Conflict Checks
    if dest.exists():
        forge_dir = dest / ".forge"
        if forge_dir.exists() and not force:
            raise FileExistsError(
                f"Target directory '{dest}' already contains .forge metadata. "
                "Refusing to overwrite without explicit confirmation (--force)."
            )
        try:
            has_files = any(dest.iterdir())
        except OSError:
            has_files = False

        if has_files and not force:
            raise FileExistsError(
                f"Target directory '{dest}' already exists and is not empty. "
                "Refusing to overwrite without explicit confirmation (--force)."
            )

    dest.mkdir(parents=True, exist_ok=True)

    # Copy and render template files
    for root, _dirs, files in os.walk(template_path):
        rel_root = Path(root).relative_to(template_path)
        dest_root = dest / rel_root
        dest_root.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = Path(root) / file
            dest_file = dest_root / file

            try:
                content = src_file.read_text(encoding="utf-8")
                rendered = content.replace("{{ project_name }}", clean_name)
                dest_file.write_text(rendered, encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                # Binary file fallback
                shutil.copy2(src_file, dest_file)

    # Ensure required Forge task directory exists
    (dest / ".forge" / "tasks").mkdir(parents=True, exist_ok=True)

    return dest
