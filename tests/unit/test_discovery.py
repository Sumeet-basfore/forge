"""Unit tests for Forge v0.2 dynamic discovery of skills and projects."""

from pathlib import Path
import pytest
import yaml

from forge.discovery import (
    discover_projects,
    discover_skills,
    extract_skill_purpose,
)


def test_discover_skills_default():
    skills = discover_skills()
    assert len(skills) >= 10
    names = [s.name for s in skills]
    assert "implementation" in names
    assert "planning" in names
    assert "testing" in names
    assert "code-review" in names

    # Check skill purpose extraction
    impl = next(s for s in skills if s.name == "implementation")
    assert "Execute precise" in impl.purpose
    assert impl.path.exists()


def test_discover_skills_custom_dir(tmp_path: Path):
    custom_skills = tmp_path / "custom_skills"
    custom_skills.mkdir()

    # Create dummy skill
    skill_a = custom_skills / "skill-a"
    skill_a.mkdir()
    (skill_a / "SKILL.md").write_text("# Skill A\n\n## Purpose\nDo thing A efficiently.\n\n## When to Use\nAlways.\n", encoding="utf-8")

    # Create dir without SKILL.md (should be ignored)
    (custom_skills / "not-a-skill").mkdir()

    discovered = discover_skills(custom_skills)
    assert len(discovered) == 1
    assert discovered[0].name == "skill-a"
    assert discovered[0].purpose == "Do thing A efficiently."


def test_discover_skills_missing_directory(tmp_path: Path):
    missing_dir = tmp_path / "does_not_exist"
    assert discover_skills(missing_dir) == []


def test_extract_skill_purpose_fallback(tmp_path: Path):
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text("# Title\n\nNo purpose section here.\n", encoding="utf-8")
    assert extract_skill_purpose(skill_file) == "No purpose specified."


def test_discover_projects_empty(tmp_path: Path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    assert discover_projects(projects_dir) == []


def test_discover_projects_missing_dir(tmp_path: Path):
    missing_dir = tmp_path / "nonexistent_projects"
    assert discover_projects(missing_dir) == []


def test_discover_projects_populated(tmp_path: Path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()

    # Valid project 1
    p1 = projects_dir / "sonora"
    p1.mkdir()
    (p1 / ".forge").mkdir()
    (p1 / ".forge" / "config.yaml").write_text(
        yaml.dump({"project": {"name": "sonora", "language": "rust"}}),
        encoding="utf-8",
    )

    # Valid project 2 (flat config format)
    p2 = projects_dir / "my_script"
    p2.mkdir()
    (p2 / ".forge").mkdir()
    (p2 / ".forge" / "config.yaml").write_text(
        yaml.dump({"project_name": "my_script", "primary_language": "python"}),
        encoding="utf-8",
    )

    # Non-forge directory
    p3 = projects_dir / "random_dir"
    p3.mkdir()

    discovered = discover_projects(projects_dir)
    assert len(discovered) == 2

    d_dict = {p.name: p for p in discovered}
    assert "sonora" in d_dict
    assert d_dict["sonora"].language == "rust"
    assert d_dict["sonora"].error is None

    assert "my_script" in d_dict
    assert d_dict["my_script"].language == "python"


def test_discover_projects_malformed_config(tmp_path: Path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()

    # Malformed YAML project (syntax error)
    p_bad = projects_dir / "broken_proj"
    p_bad.mkdir()
    (p_bad / ".forge").mkdir()
    (p_bad / ".forge" / "config.yaml").write_text("invalid_syntax: [unclosed bracket", encoding="utf-8")

    # Non-dict YAML project (e.g. list)
    p_list = projects_dir / "list_proj"
    p_list.mkdir()
    (p_list / ".forge").mkdir()
    (p_list / ".forge" / "config.yaml").write_text("- item1\n- item2\n", encoding="utf-8")

    # Valid project alongside
    p_good = projects_dir / "good_proj"
    p_good.mkdir()
    (p_good / ".forge").mkdir()
    (p_good / ".forge" / "config.yaml").write_text(
        yaml.dump({"project": {"name": "good_proj", "language": "typescript"}}),
        encoding="utf-8",
    )

    discovered = discover_projects(projects_dir)
    assert len(discovered) == 3

    bad = next(p for p in discovered if p.name == "broken_proj")
    assert bad.error is not None
    assert "Malformed configuration" in bad.error

    list_p = next(p for p in discovered if p.name == "list_proj")
    assert list_p.error is not None
    assert "root must be a YAML mapping" in list_p.error

    good = next(p for p in discovered if p.name == "good_proj")
    assert good.language == "typescript"
    assert good.error is None
